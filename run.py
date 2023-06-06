# Usage example
from IPython.core.display_functions import display

from data_frame_processor import DataFrameProcessor
from excel_manager import ExcelManager, NiceExcelFunction
from standard_gas_composition_calculations import GasComposition, PercentageO2ConsumedAndCO2ProducedAndRatio

# path_input_excel = r"C:\Users\robbe\Desktop\Q4 2022-2023\Bachelor Eind Werk\Geotechnical\Python-tool\Input Excel\Gas_production_test_KRA_Input_Robbert_04.xlsx"
# manager = ExcelManager(path_input_excel)
# manager.load_workbook()
# sheet_names = manager.get_sheet_names()
# print("Sheet names:", sheet_names)
#
# end_col = NiceExcelFunction.get_column_index("O")
# df = manager.load_sheet_table(sheet_name="GT1.1", start_row=10, end_column=end_col)
#
# display(df)



path_input_excel = r"C:\Users\robbe\Downloads\scratch try out\Gas_production_test_KRA_Input_Robbert_05tryout.xlsx"
manager = ExcelManager(path_input_excel)
manager.load_workbook()
sheet_names = manager.get_sheet_names()
print("Sheet names:", sheet_names)

end_col = NiceExcelFunction.get_column_index("O")
table_GT1_1 = manager.load_sheet_table(sheet_name="GT1.1", start_row=10, end_column=end_col)
display(table_GT1_1)

DataFrameProcessor.fill_nan_values(data_frame=table_GT1_1, column_name="Time", value="00:00:00")
DataFrameProcessor.add_day_column(data_frame=table_GT1_1, date_column_name="Date", time_column_name="Time")
display(table_GT1_1)

GasComposition.set_gas_composition(data_frame=table_GT1_1,ch4=0, co2=0.03, o2=21.90, n2=78.07)
GasComposition.sum_correct_sum(data_frame=table_GT1_1)
PercentageO2ConsumedAndCO2ProducedAndRatio.calculate_o2_consumed(data_frame=table_GT1_1)
PercentageO2ConsumedAndCO2ProducedAndRatio.calculate_co2_produced(data_frame=table_GT1_1)
PercentageO2ConsumedAndCO2ProducedAndRatio.calculate_ratio_o2_co2(data_frame=table_GT1_1)
display(table_GT1_1)

manager.make_copy_of_excel(excel_path_to_copy=path_input_excel, output_dir=r"C:\Users\robbe\Downloads\scratch try out")
# manager.replace_table_in_specific_sheet_with_data_frame(excel_file_path=path_input_excel,
#                                                         sheet_name="GT1.1",
#                                                         start_row=10,
#                                                         data_frame=table_GT1_1
#                                                         )