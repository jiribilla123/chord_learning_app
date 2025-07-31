import streamlit as st
import random

# Notes, chords and semitone data

NOTE_LETTERS = ['C', 'D', 'E', 'F', 'G', 'A', 'B']
CHORD_TYPES = {
    "": [0, 4, 7],
    "m": [0, 3, 7],
    " dim": [0, 3, 6]
}

SEMITONES = {
    'C': 0,
    'D': 2,
    'E': 4,
    'F': 5,
    'G': 7,
    'A': 9,
    'B': 11
}

# Create chords (text)

def spell_chord(root_letter, root_accidental, chord_type):
    intervals = CHORD_TYPES[chord_type]
    root_semitone = (SEMITONES[root_letter] + accidental_to_semitone(root_accidental)) % 12
    root_letter_index = NOTE_LETTERS.index(root_letter)

    spelled_notes = []

# Ensure the right note is selected (avoding for example assuming Fb as E)

    for i, interval in enumerate(intervals):
        target_semitone = (root_semitone + interval) % 12
        letter_index = (root_letter_index + i * 2) % 7
        expected_letter = NOTE_LETTERS[letter_index]
        semitone = SEMITONES[expected_letter]
        diff = (target_semitone - semitone + 12) % 12

        # Determine accidental (possible to have bb and ##)
        if diff == 0:
            accidental = ''
        elif diff <= 6:
            accidental = '#' * diff
        else:
            accidental = 'b' * (12 - diff)

        spelled_notes.append(expected_letter + accidental)

    return spelled_notes

# Ensure the right accidental direction
def accidental_to_semitone(acc):
    if acc == '#':
        return 1
    elif acc == 'b':
        return -1
    else:
        return 0

st.title("🎵 Chord Spelling Training")
st.subheader("Identify the correct notes for the given chord.")

# Session state for randomness
if "root_letter" not in st.session_state:
    st.session_state.root_letter = random.choice(NOTE_LETTERS)
    st.session_state.root_accidental = random.choice(['', '#', 'b'])
    st.session_state.chord_type = random.choice(list(CHORD_TYPES.keys()))
    st.session_state.correct_chord = spell_chord(
        st.session_state.root_letter,
        st.session_state.root_accidental,
        st.session_state.chord_type
    )

# Show the chord name
chord_name = st.session_state.root_letter + st.session_state.root_accidental + st.session_state.chord_type
st.subheader(f"{chord_name}")

# User input (still having issues to clear it after hitting the "new chord button")
user_input = st.text_input("Enter the notes in uppercase and separated by spaces (e.g. C Eb G):")
user_notes = user_input.strip().split()

# Check answer
if user_input:
    correct_notes = st.session_state.correct_chord
    if [note for note in user_notes] == [note for note in correct_notes]:
        st.success("✅ Correct!")
    else:
        st.error("❌ Incorrect")

if st.button("🎲 New Chord"):
    st.session_state.root_letter = random.choice(NOTE_LETTERS)
    
    st.session_state.root_accidental = random.choice(['', '#', 'b'])
    st.session_state.chord_type = random.choice(list(CHORD_TYPES.keys()))
    st.session_state.correct_chord = spell_chord(
        st.session_state.root_letter,
        st.session_state.root_accidental,
        st.session_state.chord_type
    )
    st.rerun()

#Personal message
st.divider()
st.markdown("Thanks for visiting 😀 I'm working on further updates including more chord variations, inversions and perhaps a better design. <br> With love ♥️🎵 <br> Jaime",unsafe_allow_html=True)

