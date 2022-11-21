class Types:
    @staticmethod
    def all_sensors():
        return {"a-kry-sensor-accelerometer", "a-kry-sensor-accelerometeruncalibrated", "a-kry-sensor-ambienttemperature", "a-kry-sensor-gps", "a-kry-sensor-gamerotationvector", "a-kry-sensor-geomagneticrotationvector", "a-kry-sensor-gravity", "a-kry-sensor-gyroscope", "a-kry-sensor-gyroscopeuncalibrated", "a-kry-sensor-light", "a-kry-sensor-linearacceleration", "a-kry-sensor-magneticfield", "a-kry-sensor-magneticfielduncalibrated", "a-kry-sensor-orientation", "a-kry-sensor-pressure", "a-kry-sensor-proximity", "a-kry-sensor-relativehumidity", "a-kry-sensor-rotationvector", "a-kry-sensor-sms", "a-kry-sensor-significantmotion", "a-kry-sensor-stepcounter", "a-kry-sensor-stepdetector", "a-kry-sensor-tiltsensor", "a-kry-sensor-wifi", "a-kry-sensor-mfcc", "a-kry-sensor-bluetooth", "a-kry-sensor-lowlatencyoffbodydetect", "a-kry-sensor-stationarydetect", "a-kry-sensor-survey", "i-kry-sensor-accelerometer", "i-kry-sensor-gyroscope", "i-kry-sensor-magnetometer", "i-kry-sensor-pedometer", "i-kry-sensor-altitude", "i-kry-sensor-location", "i-kry-sensor-compass", "i-kry-sensor-historicalactivitydata", "i-kry-sensor-accessibility", "i-kry-sensor-networkstate", "i-kry-sensor-batterystate", "i-kry-sensor-mfcc", "i-kry-sensor-survey-daily"}

    # ------------- Survey constant examples -----------------------------
    example_fever_mon = "74f6f885-c421-4106-8d16-fd32bf313637"
    example_fever_tues = "b3d73cfa-a82c-4b4d-a6cb-0e1563d4b19d"
    example_fever_wed = "c9261f75-9851-41fc-9112-84e6139b7dc4"
    example_fever_thurs = "88550559-706e-4652-99aa-bb58967864f5"
    example_fever_fri = "3dcc416b-73ef-4a28-bbbb-6af6de6710e1"
    example_fever_sat = "bc16d08a-7bfa-45f6-aedd-6c63263163a6"
    example_fever_sun = "46ec26fb-f474-40d4-9d4d-836b4b24ac0d"
    example_fever_every_day = [example_fever_mon, example_fever_tues,
                               example_fever_wed, example_fever_thurs,
                               example_fever_fri, example_fever_sat,
                               example_fever_sun]

    # ----------------------- Question UUID for Head Injuries --------------------------------------- #
    # These questions are found in the a-kry-sensor-survey-daily plain keys
    traumatic_brain_injury_question_one = "28896cdf-7c8b-43f2-a7ad-62cfffa83575"
    traumatic_brain_injury_response_one = "traumatic head injury"
    traumatic_brain_injury_question_two = "342b43b4-3a0d-4a5c-966c-a64e337e1703"
    traumatic_brain_injury_response_two = "Yes"
    traumatic_brain_injury_question_three = "3431b2f9-d858-4533-ae95-395e0d104410"
    traumatic_brain_injury_response_three = "Yes"
    traumatic_brain_injury_question_four = "c3390494-994f-47d1-a2da-f275a1ab4683"
    traumatic_brain_injury_response_four = "Yes"
    traumatic_brain_injury_questions_to_response = {
        traumatic_brain_injury_question_one: traumatic_brain_injury_response_one,
        traumatic_brain_injury_question_two: traumatic_brain_injury_response_two,
        traumatic_brain_injury_question_three: traumatic_brain_injury_response_three,
        traumatic_brain_injury_question_four: traumatic_brain_injury_response_four
    }
    compliance_message = '''Data accessed from this system contains CONTROLLED UNCLASSIFIED INFORMATION (CUI).
Please contact the system Authorizer (bbracken@cra.com) if you have any questions.
'''
