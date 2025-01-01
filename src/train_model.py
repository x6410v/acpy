import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import csv
from model import BezierAI
from src.logger import log_info, log_success, log_error
import random
import os

DATA_FILE = 'training_data.csv'

# Generate synthetic training data and save to CSV
def generate_training_data(samples=10000, save_csv=True):
    data = []
    labels = []

    for _ in range(samples):
        start = np.random.randint(0, 800, 2)
        end = np.random.randint(0, 800, 2)
        control1 = start + np.random.randint(-200, 200, 2)
        control2 = end + np.random.randint(-200, 200, 2)
        
        data.append(np.hstack([start, end]))
        labels.append(np.hstack([control1, control2]))

    if save_csv:
        with open(DATA_FILE, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['start_x', 'start_y', 'end_x', 'end_y', 'control1_x', 'control1_y', 'control2_x', 'control2_y'])
            for i in range(samples):
                writer.writerow(np.hstack([data[i], labels[i]]))
        
        log_success(f"Training data saved to {DATA_FILE}")
    
    return torch.tensor(data, dtype=torch.float32), torch.tensor(labels, dtype=torch.float32)

# Load data from CSV if it exists
def load_data_from_csv():
    if not os.path.exists(DATA_FILE):
        log_error("Training data CSV not found. Generating new data...")
        return generate_training_data()

    log_info("Loading training data from CSV...")
    X, y = [], []
    with open(DATA_FILE, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        for row in reader:
            start_end = np.array(row[:4], dtype=np.float32)
            control_points = np.array(row[4:], dtype=np.float32)
            X.append(start_end)
            y.append(control_points)

    return torch.tensor(X, dtype=torch.float32), torch.tensor(y, dtype=torch.float32)

# Train the model
def train_model(epochs=500, batch_size=64, lr=0.001):
    X, y = load_data_from_csv()

    model = BezierAI()
    optimizer = optim.Adam(model.parameters(), lr=lr)
    loss_fn = nn.MSELoss()

    dataset = torch.utils.data.TensorDataset(X, y)
    dataloader = torch.utils.data.DataLoader(dataset, batch_size=batch_size, shuffle=True)

    log_info(f"Training model for {epochs} epochs...")
    for epoch in range(epochs):
        epoch_loss = 0.0
        for batch_X, batch_y in dataloader:
            optimizer.zero_grad()
            output = model(batch_X)
            loss = loss_fn(output, batch_y)
            loss.backward()
            optimizer.step()
            epoch_loss += loss.item()

        avg_loss = epoch_loss / len(dataloader)
        log_info(f"Epoch {epoch + 1}/{epochs} - Loss: {avg_loss:.4f}")

    torch.save(model.state_dict(), 'model_weights.pth')
    log_success("Model trained and saved successfully.")

if __name__ == "__main__":
    try:
        train_model()
    except KeyboardInterrupt:
        log_error("Training interrupted by user.")