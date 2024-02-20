import pandas as pd
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Spacer, Paragraph
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
import streamlit as st
from PIL import Image
import csv
from rembg import remove
import base64
from io import BytesIO

MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB


class DiceMosaicApp:
    def __init__(self):
        self.image_path1 = None
        self.image_path2 = None
        self.image_1 = None
        self.image_2 = None
        st.set_page_config(layout="wide")
        st.sidebar.title("Center For Creative Learning")
        st.sidebar.image("DiceImages/ccl.png")
        st.title("Dice Mosaic Generator")

        self.image_path1 = st.file_uploader("Select Image 1:", type=["png", "jpg", "jpeg"])
        if self.image_path1:
            image1 = Image.open(self.image_path1)
            fixed1 = remove(image1)

            if st.button("White Background (Image 1)",type='secondary'):
                fixed1 = fixed1.convert("RGBA")
                white_background = Image.new("RGBA", fixed1.size, (255, 255, 255, 255))
                fixed1 = Image.alpha_composite(white_background, fixed1)

            if st.button("Black Background (Image 1)",type='secondary'):
                fixed1 = fixed1.convert("RGBA")
                Black_background = Image.new("RGBA", fixed1.size, (0, 0, 0, 225))
                fixed1 = Image.alpha_composite(Black_background, fixed1)
                
            buf = BytesIO()
            fixed1.save(buf, format="PNG")
            self.image_1 = fixed1
            st.image(fixed1, caption="Selected Image 1",width=300)
        
        self.image_path2 = st.file_uploader("Select Image 2:", type=["png", "jpg", "jpeg"])
        if self.image_path2:
            image2 = Image.open(self.image_path2)
            fixed2 = remove(image2)

            if st.button("White Background (Image 2)",type='secondary'):
                fixed2 = fixed2.convert("RGBA")
                white_background = Image.new("RGBA", fixed2.size, (255, 255, 255, 255))
                fixed2 = Image.alpha_composite(white_background, fixed2)
                
            if st.button("Black Background (Image 2)",type='secondary'):
                fixed2 = fixed2.convert("RGBA")
                black_background = Image.new("RGBA", fixed2.size, (0, 0, 0, 255))
                fixed2 = Image.alpha_composite(black_background, fixed2)
            buf = BytesIO()
            fixed2.save(buf, format="PNG")
            self.image_2 = fixed2
            st.image(fixed2, caption="Selected Image 2",width=300)

        if st.button("Convert to Mosaic",type='primary'):
            self.convert_to_mosaic()

        col1, col2 = st.columns(2)
        col1.write("Original Image :camera:")
        col2.write("Fixed Image :wrench:")
    def convert_to_mosaic(self):
        if self.image_path1 and self.image_path2:
            numDiceWide = 100
            numDiceTall = 100

            source_image1 = self.image_1
            source_image2 = self.image_2
            die_one = Image.open("DiceImages/1.png")
            die_two = Image.open("DiceImages/2.png")
            die_three = Image.open("DiceImages/3.png")
            die_four = Image.open("DiceImages/4.png")
            die_five = Image.open("DiceImages/5.png")
            die_six = Image.open("DiceImages/6.png")

            resized_image1 = source_image1.resize((numDiceWide, numDiceTall))
            resized_image2 = source_image2.resize((numDiceWide, numDiceTall))

            resized_image1 = resized_image1.convert('L')
            resized_image2 = resized_image2.convert('L')

            pix_val1 = list(resized_image1.getdata())
            pix_val2 = list(resized_image2.getdata())

            def map_to_dice_value(value):
                if value < 42:
                    return 1
                elif 42 <= value < 84:
                    return 2
                elif 84 <= value < 126:
                    return 3
                elif 126 <= value < 168:
                    return 4
                elif 168 <= value < 210:
                    return 5
                else:
                    return 6

            pix_val1 = [map_to_dice_value(value) for value in pix_val1]
            pix_val2 = [map_to_dice_value(value) for value in pix_val2]

            flag = 1
            for i in range(len(pix_val1)):
                if pix_val1[i] == pix_val2[i]:
                    if flag == 1:
                        flag = 0
                        if pix_val1[i] == 6:
                            pix_val1[i] = 5
                        elif pix_val1[i] == 3:
                            pix_val1[i] = 2
                        else:
                            pix_val1[i] += 1
                    else:
                        flag = 1
                        if pix_val2[i] == 6:
                            pix_val2[i] = 5
                        elif pix_val2[i] == 3:
                            pix_val2[i] = 2
                        else:
                            pix_val2[i] += 1

                elif pix_val1[i] + pix_val2[i] == 7:
                    if flag == 1:
                        flag = 0
                        if pix_val1[i] == 6:
                            pix_val1[i] = 5
                        elif pix_val1[i] == 5:
                            pix_val1[i] = 6
                        elif pix_val1[i] == 4:
                            pix_val1[i] = 5
                        elif pix_val1[i] == 3:
                            pix_val1[i] = 2
                        elif pix_val1[i] == 2:
                            pix_val1[i] = 3
                        else:
                            pix_val1[i] = 2
                    else:
                        flag = 1
                        if pix_val2[i] == 6:
                            pix_val2[i] = 5
                        elif pix_val2[i] == 5:
                            pix_val2[i] = 6
                        elif pix_val2[i] == 4:
                            pix_val2[i] = 5
                        elif pix_val2[i] == 3:
                            pix_val2[i] = 2
                        elif pix_val2[i] == 2:
                            pix_val2[i] = 3
                        else:
                            pix_val2[i] = 2

            # Calculate the size of the output image
            dice_image_width, dice_image_height = die_one.size
            output_image_size = (dice_image_width * numDiceWide, dice_image_height * numDiceTall)

            # Create black images the size of the output images
            output_image1 = Image.new('L', output_image_size, color=0)
            output_image2 = Image.new('L', output_image_size, color=0)

            # Iterate over the list and paste the correct value die onto the corresponding pixel location
            for i in range(len(pix_val1)):
                # Calculate the x_location of the top left corner of die location
                x_location = int((int(dice_image_width) * i)) % (dice_image_width * numDiceWide)
                # Calculate the y_location of the top left corner of the die image
                y_location = int(i / numDiceWide) * dice_image_height

                # Paste the die from the first image to output_image1
                if pix_val1[i] == 1:
                    output_image1.paste(die_one, (x_location, y_location))
                elif pix_val1[i] == 2:
                    output_image1.paste(die_two, (x_location, y_location))
                elif pix_val1[i] == 3:
                    output_image1.paste(die_three, (x_location, y_location))
                elif pix_val1[i] == 4:
                    output_image1.paste(die_four, (x_location, y_location))
                elif pix_val1[i] == 5:
                    output_image1.paste(die_five, (x_location, y_location))
                elif pix_val1[i] == 6:
                    output_image1.paste(die_six, (x_location, y_location))

                # Paste the die from the second image to output_image2
                if pix_val2[i] == 1:
                    output_image2.paste(die_one, (x_location, y_location))
                elif pix_val2[i] == 2:
                    output_image2.paste(die_two, (x_location , y_location))
                elif pix_val2[i] == 3:
                    output_image2.paste(die_three, (x_location , y_location))
                elif pix_val2[i] == 4:
                    output_image2.paste(die_four, (x_location , y_location))
                elif pix_val2[i] == 5:
                    output_image2.paste(die_five, (x_location , y_location))
                elif pix_val2[i] == 6:
                    output_image2.paste(die_six, (x_location , y_location))

            output_image1.save('mosaic_output1.png')
            output_image2.save('mosaic_output2.png')

            # Display the output images in the Streamlit app
            st.image('mosaic_output1.png', caption="Mosaic Image 1",width=300)
            st.image('mosaic_output2.png', caption="Mosaic Image 2",width=300)

            # Save CSV and create PDF
            pdf_path = self.save_csv_and_pdf(pix_val1, pix_val2)

            # Add a download button for the PDF
            st.download_button(
                label="Download PDF",
                data=open(pdf_path, "rb").read(),
                file_name="output.pdf",
                key="pdf_download_button"
            )

    def save_csv_and_pdf(self, pix_val1, pix_val2):
        output_pix = [int(str(val1) + str(val2)) for val1, val2 in zip(pix_val1, pix_val2)]
        num_rows = 100
        num_columns = 100
        pix_val_nested = []
        for i in range(0, len(output_pix), num_columns):
            pix_val_nested.append(output_pix[i:i + num_columns])

        csv_file_path = 'mosaic.csv'
        with open(csv_file_path, 'w', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerows(pix_val_nested)

        # Call the function to create the PDF
        pdf_path = self.create_pdf(csv_file_path)

        return pdf_path

    def create_pdf(self, csv_file_path):
        pdf_output_path = 'output.pdf'
        doc = SimpleDocTemplate(pdf_output_path, pagesize=A4)

        elements = []

        df = pd.read_csv(csv_file_path, header=None)

        rows_per_table = 10
        cols_per_table = 10

        styles = getSampleStyleSheet()
        label_style = styles['Normal']

        for start_row in range(0, len(df), rows_per_table):
            end_row = start_row + rows_per_table
            for start_col in range(0, len(df.columns), cols_per_table):
                end_col = start_col + cols_per_table

                data = df.iloc[start_row:end_row, start_col:end_col].values.tolist()

                table = Table(data)

                style = TableStyle([
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                    ('BOX', (0, 0), (-1, -1), 1, colors.black)
                ])
                table.setStyle(style)

                label = chr(ord('A') + (start_col // cols_per_table)) + str((start_row // rows_per_table) + 1)

                label_text = Paragraph(f"<b>{label}</b>", label_style)
                elements.append(label_text)
                elements.append(table)
                elements.append(Spacer(1, 35))

        doc.build(elements)

        return pdf_output_path

if __name__ == "__main__":
    app = DiceMosaicApp()
