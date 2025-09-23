---
title: RSM Simulator
emoji: 🔮
colorFrom: red
colorTo: blue
sdk: gradio
app_file: app.py
pinned: false
license: mit
---

# 🔮 RSM Simulator v2.2

**Resonant Structures of Meaning: A Machine-Executable Ontology for Interpretive AI**

This is an interactive demo of the RSM (Resonant Structures of Meaning) framework developed by the Flamehaven Initiative. RSM provides a machine-executable ontology for symbolic and interpretive AI across multiple cultural systems.

[![Live Demo](https://img.shields.io/badge/🚀-Live%20Demo-blue)](https://huggingface.co/spaces/Flamehaven/rms-simulator)
[![Paper](https://img.shields.io/badge/📄-Paper-green)](https://rsm-ontology.github.io)
[![Source Code](https://img.shields.io/badge/💻-Source%20Code-orange)](https://github.com/flamehaven/rsm-implementation)

## 🎯 What is RSM?

RSM comprises three core computational mechanisms:

1. **Vector of Meaning Energy (VME)**: Encodes symbolic representations across heterogeneous cultural systems (Tarot, Saju, Astrology)
2. **Resonance Index (RI)**: A quantitative metric of interpretive alignment and temporal stability
3. **DriftSentinel**: Monitors longitudinal deviations in symbolic consistency

## 🚀 Quick Start

### Online Demo
Simply visit our [Hugging Face Space](https://huggingface.co/spaces/Flamehaven/rms-simulator) to try RSM immediately!

### Local Installation

```bash
# Clone the repository
git clone https://github.com/flamehaven/rsm-implementation
cd rsm-implementation/huggingface_deployment

# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py
```

### Requirements
- Python 3.8+
- gradio>=5.0.0
- numpy>=1.21.0
- plotly>=5.0.0
- python-dateutil>=2.8.0

## 🔬 Technical Features

- **Real-time Calculation**: Instant symbolic reasoning with academic-grade reproducibility
- **Interactive Visualizations**: 3D energy maps, harmony trends, and cultural balance wheels
- **Multi-cultural Integration**: Seamless blending of Western and Eastern symbolic systems
- **Interpretive Analysis**: User-friendly insights based on symbolic resonance patterns
- **Drift Monitoring**: Stability assessment of symbolic interpretations
- **Complete Reproducibility**: Fixed random seeds and deterministic computation (δ < 1e-12)

## 📚 Academic Background

This demo implements the research described in:

**"Resonant Structures of Meaning: A Machine-Executable Ontology for Interpretive AI"**
*Yun Kwansub, Flamehaven Initiative (2025)*

**Version Correspondence:**
- **Paper**: RSM v2.1 methodology, Simulator suite v2.2
- **Implementation**: RSM Simulator v2.2 (this release)
- **Hugging Face Space**: Live deployment of v2.2

The framework adopts a **code-first methodology** where executable systems are treated as primary artifacts from which theoretical insights are derived.

## 🔗 Links & Resources

- [🚀 **Live Demo**](https://huggingface.co/spaces/Flamehaven/rms-simulator) - Try RSM online
- [📄 **Academic Paper**](https://rsm-ontology.github.io) - Full methodology and validation
- [💻 **Source Code**](https://github.com/flamehaven/rsm-implementation) - Complete implementation
- [🏛️ **Flamehaven Initiative**](https://flamehaven-papers.github.io) - Research organization
- [📊 **Experimental Data**](https://github.com/flamehaven/rsm-implementation/tree/main/experiments) - Validation results

## 📊 Experimental Validation

The RSM framework has been validated through comprehensive experiments:

- **VME Normalization**: 100% accuracy (norm = 1.000 ± 0.000)
- **RI Calibration**: MAE = 0.1196, False Alignment Rate = 0.000 (≤0.05 criterion met)
- **DriftSentinel**: Mean DI2 = 0.013345 across 4 test scenarios
- **LawBinder**: Mean ΔRI = +0.0110, SCG = 0.7600
- **Reproducibility**: Perfect deterministic results (δ < 1e-12)
- **Cross-cultural Validation**: Successful integration across symbolic systems

## 🎓 Citation

```bibtex
@article{flamehaven2025rsm,
  title={Resonant Structures of Meaning: A Machine-Executable Ontology for Interpretive AI},
  author={Yun, Kwansub},
  institution={Flamehaven Initiative},
  journal={arXiv preprint arXiv:2509.xxxxx},
  year={2025},
  note={Simulator suite v2.2 available at https://huggingface.co/spaces/Flamehaven/rms-simulator}
}
```

## 🏷️ Tags

`symbolic-ai` `ontology` `interpretive-ai` `cultural-systems` `tarot` `astrology` `saju` `resonance` `meaning-structures` `machine-executable` `reproducibility`

## 📋 Version History

- **v2.2** (Current): Enhanced user experience, interactive visualizations, security updates
- **v2.1**: Core RSM methodology implementation, academic validation
- **v2.0**: Initial release with basic functionality

## 🔧 Reproducibility & Testing

This implementation ensures complete reproducibility through:
- Fixed random seeds (`numpy.random.seed(42)`)
- Deterministic computation with tolerance δ < 1e-12
- Complete audit trails with SHA-256 hashing
- Versioned dependencies and test harness

For validation, run the test suite:
```bash
python -m pytest tests/ -v
```

## 📞 Contact & Support

- **Issues**: [GitHub Issues](https://github.com/flamehaven/rsm-implementation/issues)
- **Email**: info@flamehaven.space
- **Research Inquiries**: Flamehaven Initiative