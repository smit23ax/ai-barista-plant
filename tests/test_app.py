from streamlit.testing.v1 import AppTest


def test_app_runs_a_batch_and_an_ai_batch():
    at = AppTest.from_file("../app.py", default_timeout=120).run()
    assert not at.exception
    at.button[0].click().run()                         # RUN BATCH (form submit)
    assert not at.exception
    assert len(at.session_state.lab) == 1
    at.segmented_control[0].set_value("AI operator").run()
    ai_button = next(b for b in at.button if "AI: brew next batch" in b.label)
    ai_button.click().run()
    assert not at.exception
    assert len(at.session_state.ai) == 1


def test_every_view_renders():
    at = AppTest.from_file("../app.py", default_timeout=120).run()
    for view in ["Plant", "Trends", "Fluid units", "Lab notebook", "AI operator", "Engineering notes"]:
        at.segmented_control[0].set_value(view).run()
        assert not at.exception, view


def test_cavitation_alarm_trips_near_boiling():
    at = AppTest.from_file("../app.py", default_timeout=120).run()
    assert not any("CAVITATION" in e.value for e in at.error)          # 93 C default: pump is fine
    temp = next(s for s in at.slider if s.label.startswith("Kettle temperature"))
    temp.set_value(99.0)
    at.button[0].click().run()
    assert any("CAVITATION" in e.value for e in at.error)              # 99 C: NPSH margin is gone
