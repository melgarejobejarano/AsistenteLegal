import pandas as pd
from openai import OpenAI
import os

# Initialize OpenAI client
client = OpenAI()

def process_task(row):
    """Process a single task using OpenAI API"""
    try:
        # Clean up the input text
        task = str(row['tarea']).strip()
        criteria = str(row['criterio']).strip()
        
        # Combine task and criteria into a single prompt
        prompt = f"Tarea: {task}\nCriterio de respuesta: {criteria}"
        
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        return completion.choices[0].message.content.strip()
    except Exception as e:
        return f"Error processing task: {str(e)}"

def main():
    # Read the Excel file
    input_file = "Preguntitas 3.xlsx"
    output_file = "Preguntitas 3_processed.xlsx"
    
    # Read the Excel file and clean up whitespace
    df = pd.read_excel(input_file)
    df = df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
    
    # Process each row and add response
    df['respuesta'] = df.apply(process_task, axis=1)
    
    # Save the processed file
    df.to_excel(output_file, index=False)
    
    print(f"Processing complete. Results saved to {output_file}")

if __name__ == "__main__":
    main() 