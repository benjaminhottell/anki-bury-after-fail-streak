import typing

import datetime

import aqt
import anki

def get_mw() -> "aqt.AnkiQt":
    ret = aqt.mw
    assert ret is not None
    return ret

def get_col() -> "aqt.Collection":
    return get_mw().col

def get_config() -> "typing.Dict[str, typing.Any]":
    ret = get_mw().addonManager.getConfig(__name__)
    if ret is None:
        ret = {}
    return ret

def bury_cards(ids:"typing.Sequence[anki.cards.CardId]") -> None:
    assert get_mw().col is not None
    get_col().sched.buryCards(ids)

def bury_card(card_id:"anki.cards.CardId") -> None:
    bury_cards((card_id,))

def get_fail_streak(
        card_id:"anki.cards.CardId",
        fail_eases,
        max_streak:"int") -> "int":

    db = get_col().db
    assert db is not None

    revlog_entries = db.all(
        'SELECT id, ease FROM revlog WHERE cid = ? ORDER BY id DESC LIMIT ?;',
        card_id, max_streak)

    fail_streak = 0

    today_date = datetime.datetime.now()

    for (time_ms, ease) in revlog_entries:

        # skip/ignore invalid entries
        if time_ms < 0:
            continue
        if ease < 1 or ease > 4:
            continue

        # encountered a pass, so end fail streak
        if ease not in fail_eases:
            break

        fail_date = datetime.datetime.fromtimestamp(time_ms / 1000)

        # ran out of entries for today, so end fail streak
        if fail_date.day != today_date.day:
            break

        fail_streak = fail_streak + 1

    return fail_streak

def on_answer_card(
        reviewer:"aqt.reviewer.Reviewer",
        card:"anki.cards.Card",
        ease:"typing.Literal[1,2,3,4]"):

    config = get_config()

    # don't run when paused
    if config.get("paused", False):
        return

    fail_eases:"typing.Sequence[int]"
    if config.get("fail_on_hard", True):
        fail_eases = (1,2)
    else:
        fail_eases = (1,)

    # don't run when passing a card
    if not ease in fail_eases:
        return

    max_streak = config.get("streak", 3)

    fail_streak = get_fail_streak(card.id, fail_eases, max_streak)

    if fail_streak >= max_streak:
        msg = "Burying due to fail streak"
        aqt.utils.tooltip(msg);
        bury_card(card.id)

def on_toggle_pause():
    config = get_config()
    config["paused"] = not config.get("paused", False)
    get_mw().addonManager.writeConfig(__name__, config)
    aqt.utils.tooltip(f"Paused: {config['paused']}. Fail streaks aren't checked when paused.");

# Register listeners
aqt.gui_hooks.reviewer_did_answer_card.append(on_answer_card)

# Add submenu
bafs_submenu = aqt.QMenu("&Bury After Fail Streak", aqt.mw)
get_mw().form.menuTools.addMenu(bafs_submenu)

action = aqt.QAction("&Pause Toggle", aqt.mw)
action.setStatusTip("Toggle checking for fail streaks when a card is failed")
action.triggered.connect(on_toggle_pause)
bafs_submenu.addAction(action)

