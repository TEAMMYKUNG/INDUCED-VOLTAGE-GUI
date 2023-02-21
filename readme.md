## การวิเคราะห์แรงดันไฟฟ้าเหนี่ยวนำที่เกิดจากสายส่งกำลังไฟฟ้า

ANALYSIS OF THE INDUCED VOLTAGE GENERATED
BY TRASMISSION LINE.
![alt text](https://github.com/TEAMMYKUNG/INDUCED-VOLTAGE-GUI/raw/main/ui/images/2565-04-21%2011_39_36-Document1%20-%20Word.png?raw=true)
1 – 115KV Transmission line type ( PEA Thailand ) .\
2 – Max Distance of calculation in Meter Unit .\
3 – Max High of calulation in Meter Unit .\
4 – Conductor Size in Meter Unit .\
5 – Interest X -> Distanced from Center of Transmission line in Meter Unit .\
6 – Interest Y -> High frome Center of Transmission line in Meter Unit .\
7 – Calculate BTN .\
8 – Menu Bar included Help & About Us  .\
9 – Check Box Heatmap, Danger Zone Calculation .\

# Example Output
## Induce Voltage & distance in specific high
![alt text](https://github.com/TEAMMYKUNG/INDUCED-VOLTAGE-GUI/blob/main/example%20output/Case1_SS-TG-2/Figure%201.png?raw=true)
## Induced Voltage around transmission line using heatmap
![alt text](https://github.com/TEAMMYKUNG/INDUCED-VOLTAGE-GUI/blob/main/example%20output/Case1_SS-TG-2/Healpmap.png?raw=true)
## Calculate Safe Zone via induced voltage ( Touching voltage 30kV )
![alt text](https://github.com/TEAMMYKUNG/INDUCED-VOLTAGE-GUI/blob/main/example%20output/Case1_SS-TG-2/Danger%20Zone%20(%20Use%20Induce%20Voltage%20Over%2030kV%20to%20define%20zones%20).png?raw=true)
## Calculate Safe Zone via current ( Let go current )
![alt text](https://github.com/TEAMMYKUNG/INDUCED-VOLTAGE-GUI/blob/main/example%20output/Case1_SS-TG-2/Danger%20Zone%20(%20Use%20Current%20to%20define%20zones%20).png?raw=true)


## การใช้งาน (Usage)
สามารถเปิดโปรแกรมโดยใช้ Main.exe ได้เลย กรอกค่าให้เรียบร้อยเเล้วจึงกดปุ่มคำนวณ.\
Open the program using Main.exe. Fill in all text box ​​and then press the calculate button.

## การแก้ไข ( Modified Program)
ติดตั้งแพ็กเกจโดยใช้ [pip](https://pip.pypa.io/en/stable/) เพื่อติดตั้งเเพ็กเกจที่จำเป็นสำหรับโปรแกรม.\
Use the package manager [pip](https://pip.pypa.io/en/stable/) to install requirements package.
### Command Line

```bash
pip install -r requirements.txt
```
