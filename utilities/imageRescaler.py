from PIL import Image
import os

def interactive_rescale():
    # 1. Get user inputs from the console
    file_path = input("Enter the path to your image (e.g., input.png): ").strip()
    
    try:
        start_res = int(input("Enter starting resolution (e.g., 8): "))
        end_res = int(input("Enter ending resolution (e.g., 15): "))
        
        if not os.path.exists(file_path):
            print("Error: That file path doesn't exist.")
            return

        # 2. Setup output directory
        output_folder = "img/scaling/"
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        # 3. Process the image
        with Image.open(file_path) as img:
            print(f"\nProcessing {file_path}...")
            
            for res in range(start_res, end_res + 1):
                # Using NEAREST if you're doing tiny pixel-art style (7x7)
                # Change to LANCZOS for smoother photographic scaling
                rescaled_img = img.resize((res, res), Image.Resampling.NEAREST)
                
                filename = f"{res}x{res}.png"
                rescaled_img.save(os.path.join(output_folder, filename))
                print(f" -> Generated {filename}")
                
        print(f"\nSuccess! All images are in the '{output_folder}' folder.")

    except ValueError:
        print("Error: Please enter whole numbers for the resolutions.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    interactive_rescale()