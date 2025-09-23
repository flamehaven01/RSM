#!/usr/bin/env python3
"""
RSM Simulator - Hugging Face Space App
Gradio interface for Resonant Structures of Meaning demonstration
"""

import gradio as gr
import numpy as np
import json
import hashlib
from datetime import datetime, timezone
from typing import Dict, List, Tuple, Optional
import sys
import os
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots


# Fix random seed for reproducibility (δ < 1e-12)
np.random.seed(42)
# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import RSM components (simplified for HF deployment)
class SimpleVMEEngine:
    """Simplified VME Engine for Hugging Face deployment."""

    def __init__(self):
        self.symbolic_data = {
            "tarot": {
                "The Fool": {"chaos": 0.8, "rebirth": 0.9, "transformation": 0.7, "confidence": 0.85},
                "Death": {"chaos": 0.7, "rebirth": 1.0, "transformation": 1.0, "confidence": 0.95},
                "The Magician": {"chaos": 0.3, "rebirth": 0.6, "transformation": 0.9, "confidence": 0.9},
                "The Tower": {"chaos": 1.0, "rebirth": 0.7, "transformation": 0.8, "confidence": 0.9},
                "The High Priestess": {"chaos": 0.2, "rebirth": 0.8, "transformation": 0.6, "confidence": 0.8}
            },
            "astrology": {
                "Aries": {"chaos": 0.9, "rebirth": 0.8, "transformation": 0.7, "confidence": 0.85},
                "Taurus": {"chaos": 0.2, "rebirth": 0.3, "transformation": 0.4, "confidence": 0.8},
                "Gemini": {"chaos": 0.7, "rebirth": 0.6, "transformation": 0.8, "confidence": 0.75},
                "Cancer": {"chaos": 0.4, "rebirth": 0.9, "transformation": 0.6, "confidence": 0.8},
                "Leo": {"chaos": 0.6, "rebirth": 0.7, "transformation": 0.8, "confidence": 0.85},
                "Scorpio": {"chaos": 0.8, "rebirth": 1.0, "transformation": 1.0, "confidence": 0.9},
                "Pisces": {"chaos": 0.5, "rebirth": 0.8, "transformation": 0.7, "confidence": 0.7}
            },
            "saju": {
                "Fire Yang": {"chaos": 0.8, "rebirth": 0.6, "transformation": 0.9, "confidence": 0.9},
                "Water Yang": {"chaos": 0.5, "rebirth": 0.9, "transformation": 0.4, "confidence": 0.85},
                "Wood Yang": {"chaos": 0.4, "rebirth": 0.8, "transformation": 0.7, "confidence": 0.85},
                "Metal Yin": {"chaos": 0.3, "rebirth": 0.3, "transformation": 0.5, "confidence": 0.8},
                "Earth Yang": {"chaos": 0.2, "rebirth": 0.4, "transformation": 0.3, "confidence": 0.8}
            }
        }

    def calculate_vme(self, input_data: Dict) -> Tuple[np.ndarray, Dict]:
        """Calculate VME from symbolic input."""
        vectors = []
        systems = []
        confidences = []

        # Extract vectors from symbolic data
        for system, symbol in input_data.items():
            if system in self.symbolic_data and symbol in self.symbolic_data[system]:
                data = self.symbolic_data[system][symbol]
                vector = [data["chaos"], data["rebirth"], data["transformation"]]
                vectors.append(vector)
                systems.append(system)
                confidences.append(data["confidence"])

        # Calculate VME
        if vectors:
            avg_vector = np.mean(vectors, axis=0)
            # Normalize
            norm = np.linalg.norm(avg_vector)
            vme = avg_vector / norm if norm > 0 else np.array([0.577, 0.577, 0.577])
        else:
            vme = np.array([0.577, 0.577, 0.577])  # Default normalized vector

        # Calculate metadata
        metadata = {
            "systems_used": systems,
            "overall_confidence": np.mean(confidences) if confidences else 0.5,
            "vector_count": len(vectors)
        }

        return vme, metadata

def calculate_ri(vme: np.ndarray) -> float:
    """Calculate Resonance Index."""
    # Weighted projection with equal weights
    context_weights = np.array([1.0, 1.0, 1.0])
    projection = np.dot(vme, context_weights)
    norm_factor = np.linalg.norm(context_weights)

    # Calculate symbolic conflicts penalty
    chaos, rebirth, transformation = vme
    conflict_1 = abs(chaos - rebirth) * 0.15
    conflict_2 = abs(rebirth - transformation) * 0.1
    conflict_3 = abs(chaos - transformation) * 0.12
    high_chaos_penalty = max(0, chaos - 0.8) * 0.05
    low_energy_penalty = max(0, 0.2 - min(chaos, rebirth, transformation)) * 0.08

    penalty = min(0.3, conflict_1 + conflict_2 + conflict_3 + high_chaos_penalty + low_energy_penalty)

    ri = (projection / norm_factor) - penalty
    return max(0.0, min(1.0, ri))

def determine_drift_status(ri: float) -> str:
    """Determine drift status based on RI value."""
    if ri > 0.7:
        return "STABLE"
    elif ri > 0.4:
        return "WARNING"
    else:
        return "CRITICAL"

def generate_interpretation(vme: np.ndarray, ri: float, systems: List[str]) -> str:
    """Generate user-friendly interpretation of the RSM analysis."""
    chaos, rebirth, transformation = vme

    # Base interpretation with practical meaning
    if ri > 0.8:
        base = "**Excellent Harmony** - Your chosen symbols work beautifully together! This combination represents a coherent life theme with strong cultural wisdom."
        practical = "✨ **What this means:** The symbols you've selected tell a unified story. This suggests a time of clarity and purposeful direction."
    elif ri > 0.6:
        base = "**Good Alignment** - Your symbols complement each other well, with some interesting tensions that add depth to the reading."
        practical = "🎯 **What this means:** There's a clear overall message, but with nuanced layers. Pay attention to the subtle dynamics at play."
    elif ri > 0.4:
        base = "**Mixed Energies** - Your selected symbols contain both harmonious and conflicting elements, creating a complex reading."
        practical = "⚖️ **What this means:** You're likely experiencing internal conflict or facing a choice between different paths. This tension is normal and can be productive."
    else:
        base = "**Challenging Combination** - These symbols represent very different energies that may be difficult to reconcile."
        practical = "🤔 **What this means:** You might be pulled in multiple directions. Consider focusing on one area at a time, or seek balance between opposing forces."

    # Dominant dimension analysis with everyday language
    dominant_dim = np.argmax(vme)
    dimension_names = ["chaos", "rebirth", "transformation"]
    dominant = dimension_names[dominant_dim]

    dimension_insights = {
        "chaos": f"**Chaos Energy Leads** ({vme[0]:.2f}) - Your situation involves disruption, spontaneity, and breaking free from old patterns. Embrace the unexpected!",
        "rebirth": f"**Rebirth Energy Leads** ({vme[1]:.2f}) - A powerful time of renewal and fresh starts. You're shedding old skin and emerging renewed.",
        "transformation": f"**Transformation Energy Leads** ({vme[2]:.2f}) - Deliberate change and growth are highlighted. You're actively evolving and progressing."
    }

    # System-specific insights with cultural context
    system_notes = []
    if "tarot" in systems:
        system_notes.append("**Tarot** - Western mystical tradition emphasizing psychological archetypes and life journeys")
    if "astrology" in systems:
        system_notes.append("**Astrology** - Celestial influences reflecting personality traits and life timing")
    if "saju" in systems:
        system_notes.append("**Saju** - Korean traditional system based on birth elements and natural harmony")

    systems_text = " | ".join(system_notes) if system_notes else ""

    # Add explanation of the three dimensions
    dimension_guide = f"\n\n**Understanding Your Energy Profile:**\n• Chaos: {chaos:.2f} - Disruption, change, creative destruction\n• Rebirth: {rebirth:.2f} - Renewal, fresh starts, spiritual awakening\n• Transformation: {transformation:.2f} - Deliberate growth, evolution, progress"

    return f"{base}\n\n{practical}\n\n{dimension_insights[dominant]}{dimension_guide}\n\n**Cultural Systems Used:** {systems_text}"

# Initialize the VME engine
vme_engine = SimpleVMEEngine()

# Global storage for visualization data
visualization_history = {
    "timestamps": [],
    "ri_values": [],
    "vme_vectors": [],
    "systems_used": [],
    "combinations": []
}

def create_vme_3d_plot(vme: np.ndarray, systems: List[str]) -> go.Figure:
    """Create user-friendly 3D visualization of energy vector."""
    chaos, rebirth, transformation = vme

    # Create 3D scatter plot with clear annotations
    fig = go.Figure(data=[
        go.Scatter3d(
            x=[0, chaos],
            y=[0, rebirth],
            z=[0, transformation],
            mode='lines+markers',
            line=dict(color='rgb(255, 107, 53)', width=8),
            marker=dict(
                size=[8, 12],
                color=['rgb(26, 26, 46)', 'rgb(255, 107, 53)'],
                opacity=0.8
            ),
            name='Your Energy Signature',
            hovertemplate='<b>Your Symbol Energy</b><br>' +
                         'Chaos: %{x:.3f}<br>' +
                         'Rebirth: %{y:.3f}<br>' +
                         'Transformation: %{z:.3f}<br>' +
                         '<extra></extra>'
        ),
        # Add reference frame
        go.Scatter3d(
            x=[0, 1, 0, 0],
            y=[0, 0, 1, 0],
            z=[0, 0, 0, 1],
            mode='markers+text',
            marker=dict(size=4, color='lightgray', opacity=0.6),
            text=['Origin', 'Max Chaos', 'Max Rebirth', 'Max Transform'],
            textposition='top center',
            name='Reference Points',
            hoverinfo='text'
        )
    ])

    # Add energy level annotations
    energy_level = np.linalg.norm(vme)
    dominant_energy = ["Chaos", "Rebirth", "Transformation"][np.argmax(vme)]

    fig.update_layout(
        title=dict(
            text=f'Your Energy Map: {" + ".join(systems)}<br><sub>Dominant: {dominant_energy} | Overall Intensity: {energy_level:.2f}</sub>',
            x=0.5
        ),
        scene=dict(
            xaxis_title='Chaos Energy →<br><sub>(Disruption, Change)</sub>',
            yaxis_title='Rebirth Energy →<br><sub>(Renewal, Fresh Start)</sub>',
            zaxis_title='Transformation Energy →<br><sub>(Growth, Evolution)</sub>',
            xaxis=dict(range=[0, 1]),
            yaxis=dict(range=[0, 1]),
            zaxis=dict(range=[0, 1]),
            camera=dict(
                eye=dict(x=1.5, y=1.5, z=1.5)
            )
        ),
        width=500,
        height=400,
        margin=dict(l=0, r=0, t=60, b=0)
    )

    return fig

def create_ri_trend_plot() -> go.Figure:
    """Create user-friendly harmony trend chart."""
    if len(visualization_history["ri_values"]) < 2:
        # Default empty chart with helpful message
        fig = go.Figure()
        fig.add_annotation(
            x=0.5, y=0.5,
            text="Try different symbol combinations<br>to see your harmony trend!",
            showarrow=False,
            font=dict(size=14, color="gray"),
            xref="paper", yref="paper"
        )
        fig.update_layout(
            title='Your Harmony Journey',
            xaxis_title='Different Combinations Tried',
            yaxis_title='Harmony Score (%)',
            yaxis=dict(range=[0, 100], ticksuffix="%"),
            width=500,
            height=300,
            margin=dict(l=0, r=0, t=40, b=0)
        )
        return fig

    # Convert to percentage for user-friendliness
    ri_percentages = [ri * 100 for ri in visualization_history["ri_values"]]

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=list(range(1, len(ri_percentages) + 1)),
        y=ri_percentages,
        mode='lines+markers',
        name='Your Harmony Scores',
        line=dict(color='rgb(255, 107, 53)', width=3),
        marker=dict(size=8, color='rgb(26, 26, 46)'),
        hovertemplate='Combination #%{x}<br>Harmony: %{y:.1f}%<extra></extra>'
    ))

    # Add user-friendly status zones
    fig.add_hrect(y0=80, y1=100, fillcolor="lightgreen", opacity=0.2,
                  annotation_text="Excellent Harmony", annotation_position="top right")
    fig.add_hrect(y0=60, y1=80, fillcolor="lightyellow", opacity=0.2,
                  annotation_text="Good Alignment", annotation_position="top right")
    fig.add_hrect(y0=40, y1=60, fillcolor="lightorange", opacity=0.2,
                  annotation_text="Mixed Energies", annotation_position="top right")
    fig.add_hrect(y0=0, y1=40, fillcolor="lightcoral", opacity=0.2,
                  annotation_text="Challenging", annotation_position="top right")

    avg_harmony = np.mean(ri_percentages)
    fig.update_layout(
        title=f'Your Harmony Journey<br><sub>Average: {avg_harmony:.1f}% | Latest: {ri_percentages[-1]:.1f}%</sub>',
        xaxis_title='Combination Number',
        yaxis_title='Harmony Score (%)',
        yaxis=dict(range=[0, 100], ticksuffix="%"),
        width=500,
        height=300,
        margin=dict(l=0, r=0, t=60, b=0)
    )

    return fig

def create_system_radar_chart(vme: np.ndarray, input_data: Dict) -> go.Figure:
    """Create user-friendly cultural balance radar chart."""
    dimensions = ['Chaos<br><sub>(Change & Disruption)</sub>',
                 'Rebirth<br><sub>(Renewal & Fresh Starts)</sub>',
                 'Transformation<br><sub>(Growth & Evolution)</sub>']

    fig = go.Figure()

    # Add VME vector as main trace with better styling
    fig.add_trace(go.Scatterpolar(
        r=list(vme) + [vme[0]],  # Close the shape
        theta=dimensions + [dimensions[0]],
        fill='toself',
        name='Your Combined Energy',
        line=dict(color='rgb(255, 107, 53)', width=3),
        fillcolor='rgba(255, 107, 53, 0.4)',
        hovertemplate='%{theta}<br>Energy Level: %{r:.2f}<extra></extra>'
    ))

    # Add individual system contributions with cultural context
    colors = ['rgba(138, 43, 226, 0.8)', 'rgba(255, 215, 0, 0.8)', 'rgba(34, 139, 34, 0.8)']
    system_labels = {'tarot': 'Tarot (Western)', 'astrology': 'Astrology (Celestial)', 'saju': 'Saju (Korean)'}

    systems_used = []
    for i, (system, symbol) in enumerate(input_data.items()):
        if system in vme_engine.symbolic_data and symbol in vme_engine.symbolic_data[system]:
            data = vme_engine.symbolic_data[system][symbol]
            values = [data["chaos"], data["rebirth"], data["transformation"]]
            systems_used.append(system_labels[system])

            fig.add_trace(go.Scatterpolar(
                r=values + [values[0]],
                theta=dimensions + [dimensions[0]],
                name=f'{system_labels[system]}: {symbol}',
                line=dict(color=colors[i % len(colors)], width=2),
                opacity=0.8,
                hovertemplate=f'<b>{symbol}</b><br>%{{theta}}<br>Energy: %{{r:.2f}}<extra></extra>'
            ))

    # Calculate energy balance
    total_energy = np.sum(vme)
    dominant_energy = dimensions[np.argmax(vme)].split('<br>')[0]

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 1],
                ticksuffix='',
                tickmode='array',
                tickvals=[0.2, 0.4, 0.6, 0.8, 1.0],
                ticktext=['20%', '40%', '60%', '80%', '100%']
            ),
            angularaxis=dict(
                tickfont_size=10
            )
        ),
        showlegend=True,
        title=dict(
            text=f'Cultural Balance Wheel<br><sub>Dominant: {dominant_energy} | Systems: {", ".join(systems_used)}</sub>',
            x=0.5
        ),
        width=500,
        height=400,
        margin=dict(l=0, r=0, t=60, b=0),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.2,
            xanchor="center",
            x=0.5
        )
    )

    return fig

def process_rsm_input(tarot_card, astrology_sign, saju_element):
    """Process RSM input and return analysis results with visualizations."""

    # Prepare input data
    input_data = {}
    if tarot_card and tarot_card != "None":
        input_data["tarot"] = tarot_card
    if astrology_sign and astrology_sign != "None":
        input_data["astrology"] = astrology_sign
    if saju_element and saju_element != "None":
        input_data["saju"] = saju_element

    if not input_data:
        # Return empty plots for no input
        empty_fig = go.Figure()
        empty_fig.update_layout(title="Select inputs to see visualization")
        return (
            "Please select at least one symbolic input to begin analysis.",
            "", "", "", "", "",
            empty_fig, empty_fig, empty_fig
        )

    # Calculate VME and RI
    vme, metadata = vme_engine.calculate_vme(input_data)
    ri = calculate_ri(vme)
    drift_status = determine_drift_status(ri)

    # Update visualization history
    visualization_history["timestamps"].append(datetime.now())
    visualization_history["ri_values"].append(ri)
    visualization_history["vme_vectors"].append(vme.copy())
    visualization_history["systems_used"].append(metadata['systems_used'].copy())
    visualization_history["combinations"].append(f"{tarot_card}/{astrology_sign}/{saju_element}")

    # Keep only last 20 entries for performance
    if len(visualization_history["ri_values"]) > 20:
        for key in visualization_history:
            visualization_history[key] = visualization_history[key][-20:]

    # Format results
    vme_display = f"Chaos: {vme[0]:.3f} | Rebirth: {vme[1]:.3f} | Transformation: {vme[2]:.3f}"
    ri_display = f"{ri:.3f} ({ri*100:.1f}%)"
    confidence_display = f"{metadata['overall_confidence']:.2f} ({metadata['overall_confidence']*100:.0f}%)"
    systems_display = " + ".join(metadata['systems_used']) if metadata['systems_used'] else "None"

    # Generate interpretation
    interpretation = generate_interpretation(vme, ri, metadata['systems_used'])

    # Status with ASCII markers
    status_markers = {"STABLE": "[+]", "WARNING": "[!]", "CRITICAL": "[-]"}
    status_display = f"{status_markers[drift_status]} {drift_status}"

    # Create visualizations
    vme_3d_plot = create_vme_3d_plot(vme, metadata['systems_used'])
    ri_trend_plot = create_ri_trend_plot()
    radar_plot = create_system_radar_chart(vme, input_data)

    return (
        interpretation,
        vme_display,
        ri_display,
        confidence_display,
        systems_display,
        status_display,
        vme_3d_plot,
        ri_trend_plot,
        radar_plot
    )

# Create Gradio interface
def create_interface():
    with gr.Blocks(
        title="RSM Simulator - Resonant Structures of Meaning",
        theme=gr.themes.Default(),
        css="""
        .gradio-container {
            max-width: 1200px !important;
            margin: 0 auto !important;
        }
        .main-header {
            text-align: center;
            margin-bottom: 2rem;
        }
        .result-box {
            border: 2px solid #e1e5e9;
            border-radius: 12px;
            padding: 1.5rem;
            margin: 1rem 0;
            background: #f8f9fa;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .metric-display {
            font-family: 'Courier New', monospace;
            font-size: 1.2em;
            font-weight: bold;
            color: #2c3e50;
        }
        .status-display {
            font-size: 1.3em;
            font-weight: bold;
            padding: 0.5rem;
            border-radius: 8px;
        }
        .gr-button {
            background: linear-gradient(45deg, #667eea 0%, #764ba2 100%) !important;
            color: white !important;
            border: none !important;
            border-radius: 8px !important;
            font-weight: bold !important;
            padding: 0.75rem 1.5rem !important;
            font-size: 14px !important;
        }
        .gr-dropdown, .gr-dropdown-container {
            border-radius: 8px !important;
        }
        .gr-dropdown select {
            font-size: 14px !important;
            padding: 8px 12px !important;
            background-size: 12px !important;
        }
        .gr-textbox {
            border-radius: 8px !important;
        }
        .gr-textbox input, .gr-textbox textarea {
            font-size: 14px !important;
            padding: 8px 12px !important;
        }
        /* Fix oversized icons and arrows */
        .gr-form > div > div > div > label {
            font-size: 14px !important;
        }
        .gr-dropdown:after {
            width: 12px !important;
            height: 12px !important;
        }
        /* Normalize component sizes */
        .gr-block {
            font-size: 14px !important;
        }
        .gr-markdown {
            font-size: 14px !important;
        }
        .gr-markdown h1 { font-size: 24px !important; }
        .gr-markdown h2 { font-size: 20px !important; }
        .gr-markdown h3 { font-size: 18px !important; }
        .gr-markdown h4 { font-size: 16px !important; }
        /* Fix plot component sizes */
        .gr-plot {
            max-height: 400px !important;
        }
        h1, h2, h3 { color: #2c3e50 !important; }
        """
    ) as iface:

        gr.HTML("""
        <div class="main-header">
            <h1 style="color: #2c3e50; font-size: 2.5em; margin-bottom: 0.5rem;">🔮 RSM Simulator</h1>
            <h2 style="color: #34495e; font-size: 1.5em; margin-bottom: 1rem;">Discover How Cultural Symbols Resonate Together</h2>
            <p style="color: #7f8c8d; font-size: 1.1em; margin-bottom: 1rem;"><strong>Academic Research Demo</strong> | Explore the harmony between Tarot, Astrology, and Korean Saju</p>
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 15px; border-radius: 10px; margin: 15px auto; max-width: 700px; box-shadow: 0 4px 8px rgba(0,0,0,0.2);">
                <strong style="font-size: 1.1em;">💡 How to use:</strong> Select symbols from different traditions below and watch how they interact!
                Higher harmony scores mean your symbols work well together across cultures.
            </div>
        </div>
        """)

        with gr.Row(equal_height=True):
            with gr.Column(scale=1, min_width=300):
                gr.Markdown("### 🎯 Symbolic Input Selection")

                tarot_input = gr.Dropdown(
                    choices=["None", "The Fool", "Death", "The Magician", "The Tower", "The High Priestess"],
                    value="None",
                    label="🔮 Tarot Card (Western Mysticism)",
                    info="The Fool: New beginnings • Death: Transformation • Magician: Personal power • Tower: Sudden change • High Priestess: Inner wisdom"
                )

                astrology_input = gr.Dropdown(
                    choices=["None", "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Scorpio", "Pisces"],
                    value="None",
                    label="⭐ Zodiac Sign (Celestial Influences)",
                    info="Aries: Leadership • Taurus: Stability • Gemini: Communication • Cancer: Nurturing • Leo: Creativity • Scorpio: Intensity • Pisces: Intuition"
                )

                saju_input = gr.Dropdown(
                    choices=["None", "Fire Yang", "Water Yang", "Wood Yang", "Metal Yin", "Earth Yang"],
                    value="None",
                    label="☯️ Saju Element (Korean Tradition)",
                    info="Fire Yang: Dynamic energy • Water Yang: Flow and adaptation • Wood Yang: Growth and expansion • Metal Yin: Refinement • Earth Yang: Grounding"
                )

                calculate_btn = gr.Button("🧮 Calculate RSM", variant="primary", size="lg")

                gr.Markdown("""
                ### 📚 What is RSM?

                **RSM** helps you understand how different cultural symbols work together:

                **🎯 Simple Explanation:**
                - Choose symbols from **Tarot** (Western mysticism), **Astrology** (celestial influences), or **Saju** (Korean elements)
                - RSM calculates how well they "resonate" together
                - Get insights about **Chaos** (disruption), **Rebirth** (renewal), and **Transformation** (growth)

                **🔬 How It Works:**
                - **VME**: Maps your symbols to energy dimensions
                - **RI**: Scores harmony between symbols (0-100%)
                - **Graphs**: Show your energy patterns visually

                **💡 Perfect for:** Personal reflection, understanding life themes, exploring cultural wisdom
                """)

            with gr.Column(scale=2, min_width=500):
                gr.Markdown("### 📊 RSM Analysis Results")

                interpretation_output = gr.Markdown(
                    value="Select symbolic inputs and click 'Calculate RSM' to begin analysis.",
                    elem_classes=["result-box"]
                )

                with gr.Row():
                    with gr.Column(scale=1):
                        gr.Markdown("#### 🔬 Technical Metrics")
                        vme_output = gr.Textbox(
                            label="Energy Vector (Chaos | Rebirth | Transformation)",
                            value="",
                            elem_classes=["metric-display"],
                            info="Your symbols mapped to three core life energies"
                        )
                        ri_output = gr.Textbox(
                            label="Harmony Score (0-100%)",
                            value="",
                            elem_classes=["metric-display"],
                            info="How well your symbols work together"
                        )
                        confidence_output = gr.Textbox(
                            label="Reliability",
                            value="",
                            elem_classes=["metric-display"],
                            info="How trustworthy this reading is"
                        )

                    with gr.Column(scale=1):
                        gr.Markdown("#### 📋 Analysis Details")
                        systems_output = gr.Textbox(
                            label="Cultural Sources",
                            value="",
                            elem_classes=["metric-display"],
                            info="Which traditions contributed to this reading"
                        )
                        status_output = gr.Textbox(
                            label="Reading Stability",
                            value="",
                            elem_classes=["status-display"],
                            info="How stable and consistent your symbolic combination is"
                        )

                # Add visualization section with helpful descriptions
                gr.Markdown("### 📊 Visual Analysis")

                gr.Markdown("""
                **📈 Understanding Your Charts:**
                - **3D Energy Map**: See your symbols plotted in chaos/rebirth/transformation space
                - **Harmony Trend**: Track how well different combinations work over time
                - **Cultural Balance**: Compare contributions from each tradition
                """)

                with gr.Row():
                    with gr.Column():
                        vme_3d_plot = gr.Plot(
                            label="🎯 Your Energy Map (3D)",
                            value=None
                        )

                    with gr.Column():
                        ri_trend_plot = gr.Plot(
                            label="📈 Harmony History",
                            value=None
                        )

                with gr.Row():
                    radar_plot = gr.Plot(
                        label="🌍 Cultural Balance Wheel",
                        value=None
                    )

        # Event handlers
        calculate_btn.click(
            fn=process_rsm_input,
            inputs=[tarot_input, astrology_input, saju_input],
            outputs=[interpretation_output, vme_output, ri_output, confidence_output, systems_output, status_output, vme_3d_plot, ri_trend_plot, radar_plot]
        )

        # Auto-calculate on input change
        for input_component in [tarot_input, astrology_input, saju_input]:
            input_component.change(
                fn=process_rsm_input,
                inputs=[tarot_input, astrology_input, saju_input],
                outputs=[interpretation_output, vme_output, ri_output, confidence_output, systems_output, status_output, vme_3d_plot, ri_trend_plot, radar_plot]
            )

        gr.HTML("""
        <div style="text-align: center; margin-top: 2rem; padding: 1rem; background: #f5f5f5; border-radius: 8px;">
            <h3>🎓 Understanding Your Results</h3>
            <div style="text-align: left; max-width: 800px; margin: 0 auto;">
                <h4>🔍 Quick Guide:</h4>
                <ul>
                    <li><strong>Harmony Score 80-100%:</strong> Excellent combination - symbols work beautifully together</li>
                    <li><strong>Harmony Score 60-80%:</strong> Good alignment with interesting complexity</li>
                    <li><strong>Harmony Score 40-60%:</strong> Mixed energies - both harmonious and conflicting elements</li>
                    <li><strong>Harmony Score 0-40%:</strong> Challenging combination requiring careful interpretation</li>
                </ul>
                <h4>⚡ Energy Dimensions:</h4>
                <ul>
                    <li><strong>Chaos:</strong> Change, disruption, breaking patterns, creative destruction</li>
                    <li><strong>Rebirth:</strong> Renewal, fresh starts, spiritual awakening, transformation</li>
                    <li><strong>Transformation:</strong> Deliberate growth, evolution, progressive change</li>
                </ul>
            </div>
            <div style="margin-top: 1.5rem;">
                <h4>🔗 For Researchers</h4>
                <p>
                    <a href="https://rsm-ontology.github.io" target="_blank">📄 Academic Paper</a> |
                    <a href="https://github.com/flamehaven/rsm-implementation" target="_blank">💻 Source Code</a> |
                    <a href="https://flamehaven-papers.github.io" target="_blank">🏛️ Flamehaven Initiative</a>
                </p>
                <p style="font-size: 0.8em; color: #666;">
                    <strong>Reference:</strong> Flamehaven Research Team (2025). "Resonant Structures of Meaning: A Machine-Executable Ontology for Interpretive AI."
                </p>
            </div>
        </div>
        """)

    return iface

# Launch the app
if __name__ == "__main__":
    demo = create_interface()
    demo.launch(
        share=True,
        show_error=True,
        server_name="0.0.0.0",
        server_port=7860
    )