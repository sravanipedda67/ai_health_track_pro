import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import streamlit.components.v1 as components
import base64
import os
import smtplib

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Health Track Pro",
    page_icon="🏃",
    layout="wide"
)


# =========================================================
# IMAGE FUNCTION
# =========================================================

def get_img(file_path):
    try:
        with open(file_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except Exception:
        return ""


# =========================================================
# PROJECT DIRECTORY
# =========================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


# =========================================================
# LOGO
# =========================================================

logo_path = os.path.join(BASE_DIR, "cr.jpeg")
logo_img = get_img(logo_path)


# =========================================================
# FIND BANNER IMAGE AUTOMATICALLY
# =========================================================

banner_path = None

image_extensions = (
    ".jpg",
    ".jpeg",
    ".png",
    ".webp"
)

for file_name in os.listdir(BASE_DIR):

    if file_name.lower().endswith(image_extensions):

        if file_name.lower() != "cr.jpeg":

            banner_path = os.path.join(
                BASE_DIR,
                file_name
            )

            break


if banner_path:
    banner_img = get_img(banner_path)
else:
    banner_img = ""


# =========================================================
# EMAIL FUNCTION
# =========================================================

def send_health_email(
    receiver_email,
    subject,
    body
):

    try:

        sender_email = st.secrets["SENDER_EMAIL"]

        sender_password = st.secrets[
            "SENDER_APP_PASSWORD"
        ]

        message = MIMEMultipart()

        message["From"] = sender_email
        message["To"] = receiver_email
        message["Subject"] = subject

        message.attach(
            MIMEText(
                body,
                "html"
            )
        )

        # Gmail SMTP
        with smtplib.SMTP(
            "smtp.gmail.com",
            587
        ) as server:

            server.starttls()

            server.login(
                sender_email,
                sender_password
            )

            server.sendmail(
                sender_email,
                receiver_email,
                message.as_string()
            )

        return True, "Email sent successfully."

    except KeyError:

        return False, (
            "Email settings are missing. "
            "Please check .streamlit/secrets.toml"
        )

    except Exception as e:

        return False, str(e)


# =========================================================
# SIDEBAR MENU
# =========================================================

menu = st.sidebar.radio(
    "Menu",
    [
        "Home",
        "Dashboard"
    ]
)


# =========================================================
# HOME PAGE
# =========================================================

if menu == "Home":

    home_html = f"""
    <html>

    <head>

    <style>

        body {{
            margin: 0;
            padding: 0;

            background:
                radial-gradient(
                    circle at top,
                    #252525,
                    #000000
                );

            font-family: 'Segoe UI', sans-serif;
            color: white;
        }}

        .main-container {{
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 90vh;
            padding: 15px;
            box-sizing: border-box;
        }}

        .card {{
            display: flex;
            align-items: center;
            justify-content: center;

            gap: 45px;

            width: 98%;
            min-height: 650px;

            background:
                rgba(255,255,255,0.06);

            padding: 40px;

            border-radius: 30px;

            box-shadow:
                0px 0px 40px
                rgba(255,255,255,0.15);

            backdrop-filter: blur(15px);

            box-sizing: border-box;
        }}

        .logo {{
            width: 360px;
            height: 360px;

            object-fit: contain;

            border-radius: 20px;

            flex-shrink: 0;
        }}

        .content {{
            flex: 1.5;
            min-width: 0;

            text-align: left;

            display: flex;
            flex-direction: column;
            align-items: flex-start;
        }}

        .banner {{
            width: 100%;
            max-width: 1200px;

            height: 280px;

            object-fit: contain;

            object-position: center;

            border-radius: 18px;

            margin-top: -35px;
            margin-bottom: 25px;

            display: block;
        }}

        .dept {{
            color: #ffd700;

            font-size: 32px;

            font-weight: bold;

            margin-bottom: 20px;

            line-height: 1.25;
        }}

        .title {{
            font-size: 52px;

            font-weight: bold;

            margin-bottom: 25px;

            color: white;

            line-height: 1.15;
        }}

        .credits {{
            font-size: 22px;

            line-height: 1.6;

            color: #dddddd;
        }}

        .error {{
            color: #ff5555;

            font-size: 18px;

            padding: 20px;

            border: 1px solid #ff5555;

            border-radius: 10px;

            margin-bottom: 25px;
        }}

    </style>

    </head>

    <body>

        <div class="main-container">

            <div class="card">

                <img
                    src="data:image/jpeg;base64,{logo_img}"
                    class="logo"
                >

                <div class="content">

                    {
                        f'<img src="data:image/jpeg;base64,{banner_img}" class="banner">'
                        if banner_img
                        else
                        '<div class="error">❌ Banner image not found</div>'
                    }

                    <div class="dept">
                        ARTIFICIAL INTELLIGENCE & DATA SCIENCE
                    </div>

                    <div class="title">
                        AI HEALTH TRACK PRO
                    </div>

                    <div class="credits">
                        Designed by<br>
                        Sravani | Mahima Glory | Thanushka
                    </div>

                </div>

            </div>

        </div>

    </body>

    </html>
    """

    components.html(
        home_html,
        height=850,
        scrolling=False
    )


# =========================================================
# DASHBOARD
# =========================================================

elif menu == "Dashboard":

    st.title("🏃 Health-Track Pro")

    st.write(
        "AI-Based Health Monitoring & Smart Suggestions"
    )


    # =====================================================
    # SIDEBAR INPUTS
    # =====================================================

    st.sidebar.header(
        "Enter Health Data"
    )


    steps = st.sidebar.number_input(
        "Steps",
        min_value=0,
        value=0
    )


    sleep_hours = st.sidebar.number_input(
        "Sleep Hours",
        min_value=0.0,
        value=0.0,
        step=0.5
    )


    water = st.sidebar.number_input(
        "Water Intake (Litres)",
        min_value=0.0,
        value=0.0,
        step=0.1
    )


    heart_rate = st.sidebar.number_input(
        "Heart Rate (BPM)",
        min_value=0,
        value=0
    )


    weight = st.sidebar.number_input(
        "Weight (kg)",
        min_value=0.0,
        value=0.0,
        step=0.1
    )


    height = st.sidebar.number_input(
        "Height (meters)",
        min_value=0.0,
        value=0.0,
        step=0.01
    )


    analyze = st.sidebar.button(
        "🔍 Analyze Health Data"
    )


    # =====================================================
    # ANALYZE DATA
    # =====================================================

    if analyze:

        if (
            steps == 0
            or weight == 0
            or height == 0
        ):

            st.warning(
                "⚠️ Please enter valid Steps, Weight and Height."
            )

        else:

            # =================================================
            # CALCULATIONS
            # =================================================

            calories = steps * 0.04

            distance = steps * 0.0008

            bmi = weight / (height ** 2)


            # =================================================
            # BMI CATEGORY
            # =================================================

            if bmi < 18.5:

                bmi_category = "Underweight"

            elif bmi < 25:

                bmi_category = "Normal"

            elif bmi < 30:

                bmi_category = "Overweight"

            else:

                bmi_category = "Obese"


            # =================================================
            # AI FITNESS RESULT
            # =================================================

            if (
                steps >= 8000
                and sleep_hours >= 7
                and water >= 2
            ):

                prediction = "Excellent Fitness"

            elif steps >= 5000:

                prediction = "Moderate Activity"

            else:

                prediction = "Low Activity"


            # =================================================
            # SMART HEALTH SUGGESTIONS
            # =================================================

            suggestions = []


            # 1. STEPS

            if steps < 3000:

                suggestions.append(
                    "🚶 Your step count is relatively low. "
                    "Add short, comfortable walks during the day."
                )

            elif steps < 6000:

                suggestions.append(
                    "🚶 Try gradually increasing your daily "
                    "walking activity."
                )

            elif steps < 8000:

                suggestions.append(
                    "👟 You have a good amount of activity. "
                    "You can gradually increase movement if comfortable."
                )

            else:

                suggestions.append(
                    "👟 Your entered step count shows "
                    "a good level of daily movement."
                )


            # 2. SLEEP

            if sleep_hours < 5:

                suggestions.append(
                    "😴 Your entered sleep duration is quite low. "
                    "Try maintaining a regular sleep and wake schedule."
                )

            elif sleep_hours < 7:

                suggestions.append(
                    "🌙 Consider allowing more time for sleep "
                    "and keeping a consistent bedtime."
                )

            elif sleep_hours <= 9:

                suggestions.append(
                    "😴 Your entered sleep duration is within "
                    "a commonly recommended range."
                )

            else:

                suggestions.append(
                    "🛌 You entered a longer sleep duration. "
                    "Keep a consistent sleep routine and notice "
                    "how you feel during the day."
                )


            # 3. WATER

            if water < 1:

                suggestions.append(
                    "💧 Your entered fluid intake is low. "
                    "Remember to drink fluids regularly."
                )

            elif water < 2:

                suggestions.append(
                    "💧 Try drinking fluids regularly instead "
                    "of waiting until you feel very thirsty."
                )

            else:

                suggestions.append(
                    "💧 Your entered water intake shows "
                    "good attention to hydration."
                )


            # 4. HEART RATE

            if heart_rate == 0:

                suggestions.append(
                    "❤️ Enter a heart-rate value to receive "
                    "a heart-rate-related suggestion."
                )

            elif heart_rate < 60:

                suggestions.append(
                    "❤️ Your entered heart rate is below the "
                    "simple range used by this app. If this is "
                    "unusual for you or you feel unwell, discuss "
                    "it with a healthcare professional."
                )

            elif heart_rate <= 100:

                suggestions.append(
                    "❤️ Your entered heart rate falls within "
                    "the simple 60–100 BPM range used by this app."
                )

            else:

                suggestions.append(
                    "❤️ Your entered heart rate is above the "
                    "simple range used by this app. If this is "
                    "unusual or persistent, consider discussing "
                    "it with a healthcare professional."
                )


            # 5. BMI

            if bmi_category == "Underweight":

                suggestions.append(
                    "🥗 Your calculated BMI is in the underweight "
                    "category using this app's screening thresholds. "
                    "Focus on balanced nutrition and consider "
                    "professional guidance."
                )

            elif bmi_category == "Normal":

                suggestions.append(
                    "🥗 Your calculated BMI falls in the normal "
                    "category using this app's screening thresholds. "
                    "Continue with balanced nutrition and regular activity."
                )

            elif bmi_category == "Overweight":

                suggestions.append(
                    "🥗 Your calculated BMI falls in the overweight "
                    "category using this app's screening thresholds. "
                    "Focus on balanced meals and regular activity."
                )

            else:

                suggestions.append(
                    "🥗 Your calculated BMI falls in the obesity "
                    "category using this app's screening thresholds. "
                    "Consider discussing healthy lifestyle goals "
                    "with a qualified healthcare professional."
                )


            # 6. CALORIES

            if calories < 150:

                suggestions.append(
                    "🔥 Your estimated calories from the entered "
                    "steps are relatively low."
                )

            elif calories < 400:

                suggestions.append(
                    "🔥 Your entered steps contribute to daily "
                    "energy expenditure."
                )

            else:

                suggestions.append(
                    "🔥 Your entered step count represents a "
                    "higher estimated energy expenditure."
                )


            # 7. DISTANCE

            if distance < 2:

                suggestions.append(
                    "📍 Your estimated walking distance is low. "
                    "Consider adding short walks between study "
                    "or work sessions."
                )

            elif distance < 5:

                suggestions.append(
                    "📍 You have some walking activity. "
                    "Consistency is more important than making "
                    "sudden large changes."
                )

            else:

                suggestions.append(
                    "📍 Your estimated walking distance shows "
                    "substantial daily movement."
                )


            # 8

            suggestions.append(
                "⏰ Try to keep regular timings for sleep, "
                "meals, study/work, relaxation and physical activity."
            )


            # 9

            suggestions.append(
                "🪑 If you spend long periods sitting, take "
                "short movement breaks and change your posture regularly."
            )


            # 10

            suggestions.append(
                "🍎 Aim for varied, balanced meals with vegetables, "
                "fruits, grains and appropriate protein sources."
            )


            # 11

            suggestions.append(
                "🥣 If you eat breakfast, include a combination "
                "of nutritious foods rather than relying mainly "
                "on sugary foods."
            )


            # 12

            suggestions.append(
                "📱 Take regular breaks from screens, especially "
                "during long study or computer sessions."
            )


            # 13

            suggestions.append(
                "🧍 Keep a comfortable sitting posture and adjust "
                "your chair, desk and screen position when studying "
                "or working."
            )


            # 14

            suggestions.append(
                "🌳 When practical and safe, spend some time outdoors "
                "and include light physical activity in your routine."
            )


            # 15

            suggestions.append(
                "🤸 Gentle stretching or mobility exercises can be "
                "useful during breaks, especially after long periods "
                "of sitting."
            )


            # 16

            suggestions.append(
                "🧘 Include enough recovery and relaxation time "
                "in your daily routine instead of staying active continuously."
            )


            # 17

            suggestions.append(
                "📚 During long study sessions, divide your time "
                "into focused periods with short breaks."
            )


            # 18

            suggestions.append(
                "🌅 A consistent morning routine can help organize "
                "sleep, meals, hydration and daily activity."
            )


            # 19

            suggestions.append(
                "🌙 Keep your evening routine calm and consistent "
                "to support good sleep habits."
            )


            # 20

            suggestions.append(
                "🥤 Keep fluids available during the day so hydration "
                "becomes a regular habit."
            )


            # 21

            suggestions.append(
                "⚖️ Try to balance physical activity, study/work, "
                "meals, sleep and relaxation rather than focusing "
                "on only one area."
            )


            # 22

            suggestions.append(
                "📅 Consistency matters. Small healthy habits repeated "
                "regularly can be easier to maintain than sudden major changes."
            )


            # =================================================
            # FOCUS
            # =================================================

            if steps < 6000:

                focus = (
                    "🚶 Focus: Add more comfortable movement "
                    "during the day."
                )

            elif sleep_hours < 7:

                focus = (
                    "😴 Focus: Improve your sleep routine."
                )

            elif water < 2:

                focus = (
                    "💧 Focus: Pay more attention to regular hydration."
                )

            else:

                focus = (
                    "🌟 Focus: Maintain consistency across "
                    "your daily routine."
                )


            # =================================================
            # SAVE REPORT IN SESSION STATE
            # =================================================

            st.session_state["health_report"] = {

                "steps": steps,

                "sleep_hours": sleep_hours,

                "water": water,

                "heart_rate": heart_rate,

                "weight": weight,

                "height": height,

                "calories": calories,

                "distance": distance,

                "bmi": bmi,

                "bmi_category": bmi_category,

                "prediction": prediction,

                "suggestions": suggestions,

                "focus": focus
            }


# =========================================================
# DISPLAY SAVED REPORT
# =========================================================

if "health_report" in st.session_state:

    report = st.session_state["health_report"]

    steps = report["steps"]
    sleep_hours = report["sleep_hours"]
    water = report["water"]
    heart_rate = report["heart_rate"]
    weight = report["weight"]
    height = report["height"]

    calories = report["calories"]
    distance = report["distance"]
    bmi = report["bmi"]
    bmi_category = report["bmi_category"]

    prediction = report["prediction"]
    suggestions = report["suggestions"]
    focus = report["focus"]


    # =====================================================
    # HEALTH METRICS
    # =====================================================

    st.subheader(
        "📊 Health Metrics"
    )


    col1, col2, col3, col4 = st.columns(4)


    col1.metric(
        "👟 Steps",
        f"{steps:,}"
    )


    col2.metric(
        "🔥 Calories",
        f"{calories:.1f}"
    )


    col3.metric(
        "📍 Distance",
        f"{distance:.2f} km"
    )


    col4.metric(
        "⚖️ BMI",
        f"{bmi:.2f}"
    )


    st.info(
        f"📌 BMI Category: **{bmi_category}**"
    )


    # =====================================================
    # DATAFRAME
    # =====================================================

    df = pd.DataFrame({

        "Metric": [
            "Steps",
            "Sleep Hours",
            "Water (L)",
            "Heart Rate"
        ],

        "Value": [
            steps,
            sleep_hours,
            water,
            heart_rate
        ]

    })


    # =====================================================
    # GRAPH
    # =====================================================

    st.subheader(
        "📈 Daily Health Data"
    )


    fig, ax = plt.subplots(
        figsize=(10, 5)
    )


    ax.bar(
        df["Metric"],
        df["Value"]
    )


    ax.set_title(
        "Daily Health Data Overview"
    )


    ax.set_xlabel(
        "Health Metrics"
    )


    ax.set_ylabel(
        "Value"
    )


    plt.xticks(
        rotation=15
    )


    st.pyplot(fig)

    plt.close(fig)


    # =====================================================
    # AI FITNESS RESULT
    # =====================================================

    st.subheader(
        "🤖 AI Fitness Result"
    )


    if prediction == "Excellent Fitness":

        st.success(
            f"🌟 {prediction}"
        )

    elif prediction == "Moderate Activity":

        st.info(
            f"👍 {prediction}"
        )

    else:

        st.warning(
            f"📌 {prediction}"
        )


    # =====================================================
    # SMART HEALTH SUGGESTIONS
    # =====================================================

    st.subheader(
        "💡 Smart Health Suggestions"
    )


    for i, suggestion in enumerate(
        suggestions,
        start=1
    ):

        st.info(
            f"**Suggestion {i}:** {suggestion}"
        )


    # =====================================================
    # PERSONALIZED SUMMARY
    # =====================================================

    st.subheader(
        "📋 Personalized Health Summary"
    )


    positive_points = 0


    if steps >= 6000:
        positive_points += 1


    if 7 <= sleep_hours <= 9:
        positive_points += 1


    if water >= 2:
        positive_points += 1


    if 60 <= heart_rate <= 100:
        positive_points += 1


    if positive_points >= 3:

        st.success(
            "🌟 Several of your entered values show positive "
            "daily-health indicators. Continue building "
            "consistent habits."
        )

    elif positive_points >= 2:

        st.info(
            "👍 Your data shows some positive indicators. "
            "The suggestions above highlight areas you can "
            "work on gradually."
        )

    else:

        st.warning(
            "📌 Your entered values indicate several areas "
            "where healthier daily routines may be useful. "
            "Focus on small, sustainable changes."
        )


    # =====================================================
    # HEALTH CHECKLIST
    # =====================================================

    st.subheader(
        "✅ Daily Health Checklist"
    )


    check1 = steps >= 6000

    check2 = sleep_hours >= 7

    check3 = water >= 2

    check4 = 60 <= heart_rate <= 100


    st.write(
        f"{'✅' if check1 else '⬜'} Regular movement"
    )

    st.write(
        f"{'✅' if check2 else '⬜'} Adequate sleep routine"
    )

    st.write(
        f"{'✅' if check3 else '⬜'} Hydration"
    )

    st.write(
        f"{'✅' if check4 else '⬜'} Heart-rate value within "
        "app's simple reference range"
    )


    # =====================================================
    # SUGGESTED FOCUS
    # =====================================================

    st.subheader(
        "🎯 Suggested Focus"
    )


    st.write(focus)


    # =====================================================
    # EMAIL SECTION
    # =====================================================

    st.markdown("---")

    st.subheader(
        "📧 Send Health Report"
    )

    st.write(
        "Enter your friend's email address below "
        "to send this health analysis."
    )


    friend_email = st.text_input(
        "📩 Friend's Email Address",
        placeholder="example@gmail.com"
    )


    send_report = st.button(
        "📤 Send Report",
        use_container_width=True
    )


    if send_report:

        if friend_email.strip() == "":

            st.warning(
                "⚠️ Please enter your friend's email address."
            )

        else:

            # =================================================
            # CREATE EMAIL CONTENT
            # =================================================

            email_body = f"""
            <html>

            <body>

            <h2>🏃 Health Track Pro - Health Report</h2>

            <p>
            Here is the health analysis generated by
            Health Track Pro.
            </p>

            <hr>

            <h3>📊 Health Metrics</h3>

            <p>
            <b>👟 Steps:</b> {steps:,}
            </p>

            <p>
            <b>🔥 Calories:</b> {calories:.1f}
            </p>

            <p>
            <b>📍 Distance:</b> {distance:.2f} km
            </p>

            <p>
            <b>😴 Sleep Hours:</b> {sleep_hours}
            </p>

            <p>
            <b>💧 Water Intake:</b> {water} Litres
            </p>

            <p>
            <b>❤️ Heart Rate:</b> {heart_rate} BPM
            </p>

            <p>
            <b>⚖️ Weight:</b> {weight} kg
            </p>

            <p>
            <b>📏 Height:</b> {height} m
            </p>

            <p>
            <b>⚖️ BMI:</b> {bmi:.2f}
            </p>

            <p>
            <b>📌 BMI Category:</b> {bmi_category}
            </p>

            <hr>

            <h3>🤖 AI Fitness Result</h3>

            <p>
            <b>{prediction}</b>
            </p>

            <hr>

            <h3>💡 Smart Health Suggestions</h3>
            """

            for i, suggestion in enumerate(
                suggestions,
                start=1
            ):

                email_body += f"""
                <p>
                <b>Suggestion {i}:</b>
                {suggestion}
                </p>
                """


            email_body += f"""

            <hr>

            <h3>📋 Personalized Health Summary</h3>

            <p>
            The analysis contains the health indicators
            and suggestions generated from the entered data.
            </p>

            <h3>🎯 Suggested Focus</h3>

            <p>
            {focus}
            </p>

            <hr>

            <p>
            <b>Health Track Pro</b><br>
            Artificial Intelligence & Data Science
            </p>

            <p>
            <small>
            This application provides general educational
            information based on the values entered.
            It is not a medical diagnosis or a substitute
            for professional medical advice.
            </small>
            </p>

            </body>

            </html>
            """


            # =================================================
            # SEND EMAIL
            # =================================================

            with st.spinner(
                "📧 Sending report..."
            ):

                success, message = send_health_email(
                    friend_email,
                    "Health Track Pro - Health Report",
                    email_body
                )


            if success:

                st.success(
                    f"✅ Health report successfully sent to "
                    f"{friend_email}"
                )

            else:

                st.error(
                    f"❌ Email failed: {message}"
                )


    # =====================================================
    # DISCLAIMER
    # =====================================================

    st.caption(
        "ℹ️ This application provides general educational "
        "information based on the values entered. It is not "
        "a medical diagnosis or a substitute for professional "
        "medical advice."
    )