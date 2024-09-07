import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Function to calculate attention scores
def calculate_attention_scores(query, key, value):
    scores = np.dot(query, key.T)
    softmax_scores = np.exp(scores) / np.sum(np.exp(scores), axis=1, keepdims=True)
    attention_output = np.dot(softmax_scores, value)
    return scores, softmax_scores, attention_output

# Sample sentence and dummy vectors
sentence = "the animal didn't cross the street because it was too tired"
words = sentence.split()

# Dummy query, key, value vectors (random for simplicity)
query = np.random.rand(len(words), 4)
key = np.random.rand(len(words), 4)
value = np.random.rand(len(words), 4)

# Calculate attention scores
scores, softmax_scores, attention_output = calculate_attention_scores(query, key, value)

# Streamlit app
st.title("Attention Mechanism in LLMs")

# Display sentence
st.write(f"**Sentence:** {sentence}")

# Function to update frames for animation
def update_frame(frame):
    plt.clf()
    plt.title(f"Attention Mechanism - Step {frame + 1}")
    
    if frame < len(words):
        plt.imshow(scores[:frame+1], cmap='Blues', aspect='auto')
        plt.xticks(range(len(words)), words, rotation=90)
        plt.yticks(range(len(words)), words[:frame+1])
        plt.colorbar(label="Score")
        plt.xlabel("Key")
        plt.ylabel("Query")
    elif frame < 2 * len(words):
        plt.imshow(softmax_scores[:frame-len(words)+1], cmap='Greens', aspect='auto')
        plt.xticks(range(len(words)), words, rotation=90)
        plt.yticks(range(len(words)), words[:frame-len(words)+1])
        plt.colorbar(label="Softmax Score")
        plt.xlabel("Key")
        plt.ylabel("Query")
    else:
        plt.imshow(attention_output.T, cmap='Oranges', aspect='auto')
        plt.xticks(range(len(words)), words, rotation=90)
        plt.yticks(range(attention_output.shape[1]), ["Feature " + str(i) for i in range(attention_output.shape[1])])
        plt.colorbar(label="Attention Output")
        plt.xlabel("Words")
        plt.ylabel("Attention Output")

# Animation
fig = plt.figure(figsize=(10, 6))
ani = animation.FuncAnimation(fig, update_frame, frames=3*len(words), repeat=False)
st.pyplot(fig)
