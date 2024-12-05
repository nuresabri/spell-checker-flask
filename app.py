from flask import Flask, render_template, request
from heapq import nsmallest

# Helper Function to Check if a Character is a Vowel
def is_vowel(char):
    return char in "aeiou"

# Function to Compute the Penalty Score Between Two Words
def compute_penalty(word1, word2):
    n, m = len(word1), len(word2)
    dp = [[0] * (m + 1) for _ in range(n + 1)]

    # Initialize DP Table
    for i in range(1, n + 1):
        dp[i][0] = i * 2  # Gap penalty
    for j in range(1, m + 1):
        dp[0][j] = j * 2  # Gap penalty

    # Fill DP Table
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if word1[i - 1] == word2[j - 1]:  # Exact match
                dp[i][j] = dp[i - 1][j - 1]
            else:
                # Mismatch penalties
                if is_vowel(word1[i - 1]) and is_vowel(word2[j - 1]):
                    mismatch_penalty = 1
                elif not is_vowel(word1[i - 1]) and not is_vowel(word2[j - 1]):
                    mismatch_penalty = 1
                else:
                    mismatch_penalty = 3
                dp[i][j] = min(
                    dp[i - 1][j - 1] + mismatch_penalty,  # Replace
                    dp[i - 1][j] + 2,  # Insert gap in word2
                    dp[i][j - 1] + 2,  # Insert gap in word1
                )
    return dp[n][m]

# Function to Load Dictionary from File
def load_dictionary(file_path):
    with open(file_path, "r") as file:
        words = file.read().split()
    return [word.lower().strip(",.!?\"") for word in words]

# Function to Find the 10 Best Matches
def find_best_matches(input_word, dictionary):
    scores = [(word, compute_penalty(input_word, word)) for word in dictionary]
    return nsmallest(10, scores, key=lambda x: x[1])  # Get 10 lowest scores

# Flask App
app = Flask(__name__)
dictionary = []

@app.route("/", methods=["GET", "POST"])
def home():
    suggestions = None
    user_word = ""
    if request.method == "POST":
        user_word = request.form["word"].strip().lower()
        if user_word:
            suggestions = find_best_matches(user_word, dictionary)
    return render_template("index.html", suggestions=suggestions, user_word=user_word)

if __name__ == "__main__":
    DICTIONARY_PATH = "dictionary.txt"
    try:
        dictionary = load_dictionary(DICTIONARY_PATH)
        print(f"Loaded {len(dictionary)} words from the dictionary.")
    except FileNotFoundError:
        print(f"Error: Dictionary file '{DICTIONARY_PATH}' not found.")
        exit(1)

    app.run(debug=True)
 
