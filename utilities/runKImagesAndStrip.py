import subprocess
import os

"""
THIS FUNCTION IS FOR C++ ONLY! 
USE runKImagesPython.py FOR main.py TESTING.
"""

def run_seam_range(start_k, end_k, image_folder="img/scaling/",algo="pd", iterations="1"):
    results = []

    print(f"Targeting resolutions from {start_k}x{start_k} to {end_k}x{end_k}...\n")

    for k in range(start_k, end_k + 1):
        # Construct the filename based on the naming convention kxk.png
        img_name = f"{k}x{k}.png"
        full_path = os.path.join(image_folder, img_name)

        # Check if the specific file exists before trying to run the exe
        if not os.path.exists(full_path):
            print(f"Skipping: {img_name} (File not found)")
            continue

        command = [
            "./seam", 
            "--imagen", full_path, 
            "--algoritmo", algo, 
            "--iteraciones", str(iterations)
        ]

        try:
            process = subprocess.run(command, capture_output=True, text=True, check=True)
            
            # Clean the output and store it
            clean_output = process.stdout.strip()
            results.append({
                "resolution": k,
                "output": clean_output
            })
            print(f"Processed {k}x{k}: {clean_output}")

        except subprocess.CalledProcessError as e:
            print(f"Error running {img_name}: {e.stderr.strip()}")
            results.append({"resolution": k, "output": None})

    return results

if __name__ == "__main__":
    # Get range from user
    try:
        low = int(input("Start at resolution (k): "))
        high = int(input("End at resolution (k): "))
        iters = input("Iterations: ")
        algorithm = input("Algorithm: ")
        final_data = run_seam_range(low, high, "img/scaling/", algorithm, iters)

        # Example of how to access the list later
        print("\n--- Execution Summary ---")
        for entry in final_data:
            print(f"Res: {entry['resolution']} | Data: {entry['output']}")
            
    except ValueError:
        print("Please enter valid integers for the range.")