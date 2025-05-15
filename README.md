
# Sentiment Analysis Project
This repository contains an end-to-end Sentiment Analysis API that uses a trained machine
learning model to classify the sentiment of input text as positive, negative, or neutral. It is built
using Flask and includes all necessary modules for inference.
1. Clone the Repository


```bash
git clone https://github.com/sunny2708/sentiment_analysis_project.git

```




2. Create and Activate Conda Environment
```bash
conda create -n myenv python=3.11
conda activate myenv
```
3. Install Requirements
```bash
pip install -r requirement.txt
```

## Model Training
```bash
cd training_script
python train.py
```

## Run Flask API
After training of model done
```
cd ..
python app.py

```

Run curl command on terminal
--Note check yourl curl command according to server name 
```
curl -X POST http://127.0.0.1:8501/predict \
     -H "Content-Type: application/json" \
     -d '{"text": "I really love this product! It works great."}'
```

Output
```
{
"predicted
_
sentiment": "Postive"
,
"confidence
score": 0.8649
_
}
