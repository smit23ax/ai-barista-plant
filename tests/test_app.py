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
    for view in ["Plant", "Trends", "Fluid units", "Lab notebook", "AI operator", "Presenter", "Engineering notes"]:
        at.segmented_control[0].set_value(view).run()
        assert not at.exception, view


def test_plug_alarm_trips_for_fine_grind_and_fast_plunge():
    at = AppTest.from_file("../app.py", default_timeout=120).run()
    assert not any("PLUGGED" in e.value for e in at.error)            # standard recipe plunges easily
    next(s for s in at.slider if s.label.startswith("Grind size")).set_value(300)
    next(s for s in at.slider if s.label.startswith("Plunge time")).set_value(3)
    next(s for s in at.slider if s.label.startswith("Fines")).set_value(0.40)
    at.button[0].click().run()
    assert any("PLUGGED" in e.value for e in at.error)


def test_presenter_clicks_through_every_step_and_grill_me():
    from plant.steps import UNITS
    at = AppTest.from_file("../app.py", default_timeout=120).run()
    at.segmented_control[0].set_value("Presenter").run()
    for name, unit in UNITS.items():
        at.selectbox(key="p_unit").set_value(name).run()
        assert at.session_state.p_i == 0
        for i in range(1, len(unit["steps"])):
            at.button(key="p_next").click().run()
            assert not at.exception, (name, i)
            assert at.session_state.p_i == i
            assert unit["steps"][i]["write"] in at.latex[0].value
        assert at.button(key="p_next").disabled
        at.toggle(key="p_grill").set_value(True).run()
        assert not at.exception
        assert len(at.expander) == len(unit["questions"])
        at.toggle(key="p_grill").set_value(False).run()
