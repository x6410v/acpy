import torch
import torch.nn as nn

class BezierAI(nn.Module):
    def __init__(self):
        super(BezierAI, self).__init__()
        self.model = nn.Sequential(
            nn.Linear(4, 128),
            nn.ReLU(),
            nn.Linear(128, 256),
            nn.ReLU(),
            nn.Linear(256, 4)
        )
    
    def forward(self, x):
        return self.model(x)

def load_model():
    model = BezierAI()
    model.load_state_dict(torch.load('model_weights.pth', weights_only=True))
    model.eval()
    return model

def generate_control_points(start, end):
    model = load_model()
    input_data = torch.tensor([start[0], start[1], end[0], end[1]], dtype=torch.float32)
    output = model(input_data).detach().numpy()
    return [(output[0], output[1]), (output[2], output[3])]