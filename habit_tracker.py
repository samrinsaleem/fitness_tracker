import streamlit as st
from datetime import datetime, timedelta
import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns
from dateutil import parser

st.set_page_config(page_title="Fitness Habit Tracker", page_icon="🏋️‍♀️", layout="centered")

st.title("🏋️‍♀️ Samrin's Fitness Habit Tracker")

today_display = datetime.today().strftime("%A, %B %d, %Y")
today_date = datetime.today().date()

st.subheader(f"Today's Date: {today_display}")

# --- Period Pause ---
period_pause = st.checkbox("I'm on my period", help="Select this if you're on your period. This changes the workout to rest or stretching.")
if period_pause:
    st.markdown("**Workout of the Day:** Rest or Stretching")
else:
    # Workout of the Day
    day_of_week = datetime.today().strftime("%A")
    workout_schedule = {
        "Monday": "Full Body Strength (Arms & Core Focus)",
        "Tuesday": "Lower Body Strength (Legs, Thighs, Butt)",
        "Wednesday": "Upper Body Strength",
        "Thursday": "Glutes and Hamstrings",
        "Friday": "Cardio (Low-Impact)",
        "Saturday": "Active Recovery",
        "Sunday": "Rest or Light Stretching"
    }
    today_workout = workout_schedule.get(day_of_week, "Rest or Light Activity")
    st.markdown(f"**Workout of the Day:** [{today_workout}](#)")

    if st.button("View Workout Details"):
        st.markdown(f"### {today_workout} Details")
        if today_workout == "Full Body Strength (Arms & Core Focus)":
            st.markdown("Warm-up: 5-minute light cardio (jumping jacks, high knees)")
            st.markdown("Circuit 1:")
            st.markdown("- Dumbbell shoulder press (1 kg or 2 kg, 3 sets of 12 reps)")
            st.markdown("- Dumbbell rows (3 sets of 12 reps)")
            st.markdown("- Plank (hold for 30 seconds, 3 sets)")
            st.markdown("Circuit 2:")
            st.markdown("- Bicep curls (1 kg or 2 kg, 3 sets of 12 reps)")
            st.markdown("- Russian twists (3 sets of 15 reps per side)")
            st.markdown("- Bicycle crunches (3 sets of 15 reps)")
            st.markdown("Cool down: 5-minute stretching, focusing on arms and core")
        elif today_workout == "Lower Body Strength (Legs, Thighs, Butt)":
            st.markdown("Warm-up: 5-minute light cardio (jumping jacks, high knees)")
            st.markdown("Circuit 1:")
            st.markdown("- Squats (bodyweight or with dumbbells, 3 sets of 15 reps)")
            st.markdown("- Glute bridges (3 sets of 15 reps)")
            st.markdown("- Lunges (3 sets of 12 reps per leg)")
            st.markdown("Circuit 2:")
            st.markdown("- Donkey kicks (3 sets of 12 reps per leg)")
            st.markdown("- Side leg raises (3 sets of 15 reps per leg)")
            st.markdown("- Wall sits (hold for 30 seconds, 3 sets)")
            st.markdown("Cool down: Stretch quads, hamstrings, glutes, and calves for 5 minutes")
        elif today_workout == "Upper Body Strength":
            st.markdown("Warm-up: 5-minute light cardio (jumping jacks, high knees)")
            st.markdown("Circuit 1:")
            st.markdown("- Dumbbell chest press (1 kg or 2 kg, 3 sets of 12 reps)")
            st.markdown("- Dumbbell lateral raises (1 kg or 2 kg, 3 sets of 12 reps)")
            st.markdown("- Tricep dips (using a bench or chair, 3 sets of 12 reps)")
            st.markdown("Circuit 2:")
            st.markdown("- Dumbbell rows (3 sets of 12 reps)")
            st.markdown("- Arm circles (3 sets of 30 seconds in each direction)")
            st.markdown("- Push-ups (modify on knees if necessary, 3 sets of 10 reps)")
            st.markdown("Cool down: Stretch arms, shoulders, and back for 5 minutes")
        elif today_workout == "Cardio (Low-Impact)":
            st.markdown("30 minutes of light-to-moderate intensity cardio such as:")
            st.markdown("- Walking on a treadmill")
            st.markdown("- Cycling")
            st.markdown("- Swimming")
            st.markdown("The goal here is to keep your heart rate up without overexerting yourself.")
        elif today_workout == "Total Body Workout":
            st.markdown("Warm-up: 5-minute light cardio (jumping jacks, high knees)")
            st.markdown("Circuit 1:")
            st.markdown("- Squat jumps (3 sets of 12 reps)")
            st.markdown("- Dumbbell rows (3 sets of 12 reps)")
            st.markdown("- Mountain climbers (3 sets of 30 seconds)")
            st.markdown("Circuit 2:")
            st.markdown("- Push-ups (3 sets of 12 reps)")
            st.markdown("- Plank with leg lift (3 sets of 10 reps per leg)")
            st.markdown("- High knees (3 sets of 30 seconds)")
            st.markdown("Cool down: Stretch entire body for 5 minutes")
        elif today_workout == "Active Recovery":
            st.markdown("Gentle yoga or stretching for 30 minutes. Focus on flexibility and relaxation.")
        elif today_workout == "Rest or Light Stretching":
            st.markdown("Take this day to rest or do very light yoga/stretching if you feel up to it.")

# --- Daily Checklist ---
st.subheader("Daily Checklist:")

water_0_5 = st.checkbox("0.5L of Water")
water_1_0 = st.checkbox("1.0L of Water")
water_1_5 = st.checkbox("1.5L of Water")
water_2_0 = st.checkbox("2.0L of Water")

breakfast_done = st.checkbox("Breakfast Tracked")
lunch_done = st.checkbox("Lunch Tracked")
snack_done = st.checkbox("Snack Tracked")
dinner_done = st.checkbox("Dinner Tracked")

workout_done = st.checkbox("Workout Completed")
stretching_done = st.checkbox("Stretching Completed")

# --- Goals (Partial Accepted) ---
water_count = sum([water_0_5, water_1_0, water_1_5, water_2_0])
meals_count = sum([breakfast_done, lunch_done, snack_done, dinner_done])

water_goal_done = water_count == 4
nutrition_goal_done = meals_count == 4

if water_goal_done:
    st.success("Water Goal Reached!")
else:
    st.info(f"Water intake progress: {water_count}/4 milestones.")

if nutrition_goal_done:
    st.success("Nutrition Goal Reached!")
else:
    st.info(f"Meals tracked: {meals_count}/4 meals.")

# --- Save Section ---
st.subheader("Save Your Progress:")

default_save_path = ".\Habit.csv"
save_folder = st.text_input("File Path:", default_save_path)

if st.button("Save Progress"):
    data = {
        "Date": [today_date],
        "Workout Done": [workout_done],
        "Water 0.5L": [water_0_5],
        "Water 1.0L": [water_1_0],
        "Water 1.5L": [water_1_5],
        "Water 2.0L": [water_2_0],
        "Breakfast": [breakfast_done],
        "Lunch": [lunch_done],
        "Snack": [snack_done],
        "Dinner": [dinner_done],
        "Stretching Done": [stretching_done],
        "Water Milestones": [water_count],
        "Meals Tracked": [meals_count],
        "Water Goal Done": [water_goal_done],
        "Nutrition Goal Done": [nutrition_goal_done]
    }
    df_today = pd.DataFrame(data)

    if os.path.exists(save_folder):
        existing_df = pd.read_csv(save_folder)
        # Remove today's entry if it already exists
        existing_df = existing_df[existing_df['Date'] != str(today_date)]  
        # Append today's data as a new row
        updated_df = pd.concat([existing_df, df_today], ignore_index=True)
    else:
        updated_df = df_today

    updated_df.to_csv(save_folder, index=False)
    st.success("✅ Progress saved successfully!")
    st.balloons()

# Calculate Streak Button
if st.button("Calculate Streaks"):
    def calculate_streak(df, goal_column):
        df = df.sort_values(by="Date", ascending=False)
        streak = 0
        yesterday = datetime.today().date() - timedelta(days=1)

        for _, row in df.iterrows():
            try:
                if pd.isna(row["Date"]):
                    continue  # Skip if Date is missing
                row_date = parser.parse(str(row["Date"])).date()
            except ValueError:
                row_date = parser.parse(row["Date"]).date()

            if row_date == yesterday:
                if row[goal_column]:
                    streak += 1
                    yesterday = row_date - timedelta(days=1)
                else:
                    break
        return streak

    if os.path.exists(save_folder):
        df_progress = pd.read_csv(save_folder)

        workout_streak = calculate_streak(df_progress, "Workout Done")
        water_streak = calculate_streak(df_progress, "Water Goal Done")
        nutrition_streak = calculate_streak(df_progress, "Nutrition Goal Done")
        stretch_streak = calculate_streak(df_progress, "Stretching Done")

        col1, col2 = st.columns(2)
        with col1:
            st.metric("🏋️‍♀️ Workout Streak", f"{workout_streak} days")
            st.metric("💧 Water Streak", f"{water_streak} days")
        with col2:
            st.metric("🍽️ Nutrition Streak", f"{nutrition_streak} days")
            st.metric("🧘‍♀️ Stretching Streak", f"{stretch_streak} days")

        st.divider()

# --- Display Progress Charts ---
if os.path.exists(save_folder):
    st.subheader("📈 Progress Charts:")

    df_progress = pd.read_csv(save_folder)

    fig, axs = plt.subplots(2, 2, figsize=(12, 8))

    sns.lineplot(x="Date", y="Water Milestones", data=df_progress, marker="o", ax=axs[0, 0])
    axs[0, 0].set_title("Water Intake Milestones")
    axs[0, 0].set_ylim(0, 4)

    sns.lineplot(x="Date", y="Meals Tracked", data=df_progress, marker="o", ax=axs[0, 1])
    axs[0, 1].set_title("Meals Tracked")

    sns.barplot(x="Date", y="Workout Done", data=df_progress, ax=axs[1, 0])
    axs[1, 0].set_title("Workout Completion")

    sns.barplot(x="Date", y="Stretching Done", data=df_progress, ax=axs[1, 1])
    axs[1, 1].set_title("Stretching Completion")

    for ax in axs.flat:
        for label in ax.get_xticklabels():
            label.set_rotation(45)
    plt.tight_layout()

    st.pyplot(fig)