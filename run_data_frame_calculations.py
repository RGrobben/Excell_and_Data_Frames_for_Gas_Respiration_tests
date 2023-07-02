from data_frame_processor import DataFrameProcessor
from data_frame_calculations import PercentageO2ConsumedAndCO2ProducedAndRatio, \
    MolesProduced, CumulativeProductionGasPhase, CarbonInAqueousPhase, \
    ResultsInterpretations
from data_frame_calculations_standard_for_gas_respiration_tests import GasComposition, MolGasCompositionCalculations
import pandas as pd


class RunDataFrameCalculationsForOneDataFrame:
    """"run the calculations on one data frame"""
    data_frame: object

    def __init__(self, data_frame):
        self.data_frame = data_frame

        self.get_column_name_date: str = "Date"
        self.get_name_column_time: str = "Time"
        self.get_name_column_ch4: str = "CH4 [%]"
        self.get_name_column_co2: str = "CO2 [%]"
        self.get_name_column_o2: str = "O2 [%]"
        self.get_name_column_n2: str = "N2 [%]"
        self.get_name_column_flush: str = "Flush (1=yes; 0=no)"
        self.get_column_name_pressure_before: str = "P sample before gc [hPa]"
        self.get_column_name_pressure_after: str = "P sample after gc [hPa]"

        self.create_name_column_summation_correction: str = "Sum-corr [%]"
        self.create_name_correction_ch4: str = "CH4-corr [%]"
        self.create_name_correction_co2: str = "CO2-corr [%]"
        self.create_name_correction_o2: str = "O2-corr [%]"
        self.create_name_correction_n2: str = "N2-corr [%]"

        self.create_name_column_mg_bs: str = "mg_bs"
        self.create_name_column_mg_as: str = "mg_as"
        self.create_name_column_mCO2_b: str = "mCO2_b"
        self.create_name_column_mCH4_b: str = "mCH4_b"
        self.create_name_column_mO2_b: str = "mO2_b"
        self.create_name_column_mN2_b: str = "mN2_b"
        self.create_name_column_mCO2_a: str = "mCO2_a"
        self.create_name_column_mCH4_a: str = "mCH4_a"
        self.create_name_column_mO2_a: str = "mO2_a"
        self.create_name_column_mN2_a: str = "mN2_a"

        self.create_name_column_CTot_b: str = "mCTot_b"
        self.create_name_column_cTot_a: str = "mCTot_a"
        self.create_name_column_mCTot_produced: str = "mCTot_produced"
        self.create_name_column_oxygen_consumed: str = "O2 consumed"
        self.create_name_name_column_carbon_dioxide_produced: str = "CO2 produced"

        self.create_name_column_oxygen_consumed_cumulative: str = "O2 consumed_cum"
        self.create_name_column_C_dioxide_produced_cumulative: str = "CO2 produced_cum"
        self.create_name_column_C_total_produced_cumulative: str = "mCTot_produced_cum"
        self.create_name_column_C_gas_dry_mass_cumulative: str = "Cgas_DM_cum"

        self.create_name_column_PP_CO2_bs: str = "PP CO2_b "
        self.create_name_column_CO2_before_aq_mol_per_m3: str = "CO2_b_aq [mol/m3]"
        self.create_name_column_CO2_before_aq_mol: str = "CO2_b_aq [mol]"
        self.create_name_column_PP_CO2_as: str = "PP CO2_a "
        self.create_name_column_CO2_after_aq_mol_per_m3: str = "CO2_a_aq [mol/m3]"
        self.create_name_column_CO2_after_aq_mol: str = "CO2_a_aq [mol]"
        self.create_name_column_CO2_dissolved_between_time_steps_aq: str = "CO2_dissolved_between_time_steps_aq"
        self.create_name_column_CO2_produced_aq_cum: str = "CO2_produced_aq_cum"
        self.create_name_column_DIC_cum: str = "DIC_cum"

        self.create_name_column_Ctot_DM: str = "Ctot_DM [mg C/gDW]"
        self.create_name_column_ratio_O2_CO2: str = "Ratio O2/CO2"

    def run_data_frame_processor_calculations(self, dayfirst: bool = False):
        DataFrameProcessor.add_day_column(data_frame=self.data_frame, date_column_name=self.get_column_name_date,
                                          time_column_name=self.get_name_column_time, dayfirst=dayfirst)

    def run_gas_composition_calculations(self,
                                         set_values_gas_composition_first_row: bool = False,
                                         ch4: float = 0, co2: float = 0, o2: float = 0, n2: float = 0,
                                         index: int = 0,
                                         ):
        # set the values of the first row for the gas composition.
        if set_values_gas_composition_first_row:
            GasComposition.set_gas_composition(data_frame=self.data_frame,
                                               ch4=ch4, co2=co2, o2=o2, n2=n2, index=index,
                                               name_column_ch4=self.get_name_column_ch4,
                                               name_column_co2=self.get_name_column_co2,
                                               name_column_o2=self.get_name_column_o2,
                                               name_column_n2=self.get_name_column_n2,
                                               )

        GasComposition.sum_correct_sum(data_frame=self.data_frame,
                                       name_column_ch4=self.get_name_column_ch4,
                                       name_column_co2=self.get_name_column_co2,
                                       name_column_o2=self.get_name_column_o2,
                                       name_column_n2=self.get_name_column_n2,
                                       name_column_summation_correction=self.create_name_column_summation_correction,
                                       name_correction_ch4=self.create_name_correction_ch4,
                                       name_correction_co2=self.create_name_correction_co2,
                                       name_correction_o2=self.create_name_correction_o2,
                                       name_correction_n2=self.create_name_correction_n2
                                       )

    def run_mol_gases_before_and_after_sampling(self,
                                                Rgas: float,
                                                exp_temperature: float,
                                                volume_headspace: float,
                                                ):
        # moles gas before sampling
        MolGasCompositionCalculations.mol_gas_sampling(data_frame=self.data_frame,
                                                       Rgas=Rgas,
                                                       exp_temperature=exp_temperature,
                                                       volume_headspace=volume_headspace,
                                                       column_name_pressure=self.get_column_name_pressure_before,
                                                       name_column=self.create_name_column_mg_bs
                                                       )

        # moles gas after sampling
        MolGasCompositionCalculations.mol_gas_sampling(data_frame=self.data_frame,
                                                       Rgas=Rgas,
                                                       exp_temperature=exp_temperature,
                                                       volume_headspace=volume_headspace,
                                                       column_name_pressure=self.get_column_name_pressure_after,
                                                       name_column=self.create_name_column_mg_as
                                                       )

    def run_mol_gas_composition_calculation(self):
        # CO2 before
        MolGasCompositionCalculations.specific_gas_in_moles_before_sampling(data_frame=self.data_frame,
                                                                            name_column=self.create_name_column_mCO2_b,
                                                                            name_column_mg_before_or_after=
                                                                            self.create_name_column_mg_bs,
                                                                            name_column_specific_gas_corrected=
                                                                            self.create_name_correction_co2)
        # CH4 before
        MolGasCompositionCalculations.specific_gas_in_moles_before_sampling(data_frame=self.data_frame,
                                                                            name_column=self.create_name_column_mCH4_b,
                                                                            name_column_mg_before_or_after=
                                                                            self.create_name_column_mg_bs,
                                                                            name_column_specific_gas_corrected=
                                                                            self.create_name_correction_ch4)
        # O2 before
        MolGasCompositionCalculations.specific_gas_in_moles_before_sampling(data_frame=self.data_frame,
                                                                            name_column=self.create_name_column_mO2_b,
                                                                            name_column_mg_before_or_after=
                                                                            self.create_name_column_mg_bs,
                                                                            name_column_specific_gas_corrected=
                                                                            self.create_name_correction_o2)
        # N2 before
        MolGasCompositionCalculations.specific_gas_in_moles_before_sampling(data_frame=self.data_frame,
                                                                            name_column=self.create_name_column_mN2_b,
                                                                            name_column_mg_before_or_after=
                                                                            self.create_name_column_mg_bs,
                                                                            name_column_specific_gas_corrected=
                                                                            self.create_name_correction_n2)
        # total carbon before
        MolGasCompositionCalculations.carbon_total_moles(data_frame=self.data_frame,
                                                         name_column=self.create_name_column_CTot_b,
                                                         name_column_CO2=self.create_name_column_mCO2_b,
                                                         name_column_CH4=self.create_name_column_mCH4_b)

        # CO2 after
        MolGasCompositionCalculations.specific_gas_in_moles_before_sampling(data_frame=self.data_frame,
                                                                            name_column=self.create_name_column_mCO2_a,
                                                                            name_column_mg_before_or_after=
                                                                            self.create_name_column_mg_as,
                                                                            name_column_specific_gas_corrected=
                                                                            self.create_name_correction_co2)
        # CH4 after
        MolGasCompositionCalculations.specific_gas_in_moles_before_sampling(data_frame=self.data_frame,
                                                                            name_column=self.create_name_column_mCH4_a,
                                                                            name_column_mg_before_or_after=
                                                                            self.create_name_column_mg_as,
                                                                            name_column_specific_gas_corrected=
                                                                            self.create_name_correction_ch4)
        # O2 after
        MolGasCompositionCalculations.specific_gas_in_moles_before_sampling(data_frame=self.data_frame,
                                                                            name_column=self.create_name_column_mO2_a,
                                                                            name_column_mg_before_or_after=
                                                                            self.create_name_column_mg_as,
                                                                            name_column_specific_gas_corrected=
                                                                            self.create_name_correction_o2)
        # N2 after
        MolGasCompositionCalculations.specific_gas_in_moles_before_sampling(data_frame=self.data_frame,
                                                                            name_column=self.create_name_column_mN2_a,
                                                                            name_column_mg_before_or_after=
                                                                            self.create_name_column_mg_as,
                                                                            name_column_specific_gas_corrected=
                                                                            self.create_name_correction_n2)
        # total carbon before
        MolGasCompositionCalculations.carbon_total_moles(data_frame=self.data_frame,
                                                         name_column=self.create_name_column_cTot_a,
                                                         name_column_CO2=self.create_name_column_mCO2_a,
                                                         name_column_CH4=self.create_name_column_mCH4_a)

        # reposition the column
        DataFrameProcessor.replace_position_column(data_frame=self.data_frame,
                                                   name_replaced_column=self.create_name_column_mg_as,
                                                   name_column_of_position=self.create_name_column_mCO2_a)

    def run_moles_produced(self):
        MolesProduced.total_carbon_produced_moles(data_frame=self.data_frame,
                                                  name_column=self.create_name_column_mCTot_produced,
                                                  name_column_mCTot_b=self.create_name_column_CTot_b,
                                                  name_column_mCTot_a=self.create_name_column_cTot_a,
                                                  name_column_flush=self.get_name_column_flush
                                                  )
        MolesProduced.oxygen_consumed_moles(data_frame=self.data_frame,
                                            name_column=self.create_name_column_oxygen_consumed,
                                            name_column_mO2_b=self.create_name_column_mO2_b,
                                            name_column_mO2_a=self.create_name_column_mO2_a,
                                            name_column_flush=self.get_name_column_flush
                                            )
        MolesProduced.carbon_dioxide_produced_moles(data_frame=self.data_frame,
                                                    name_column=self.create_name_name_column_carbon_dioxide_produced,
                                                    name_column_mCO2_b=self.create_name_column_mCO2_b,
                                                    name_column_mCO2_a=self.create_name_column_mCO2_a,
                                                    name_column_flush=self.get_name_column_flush
                                                    )

    def run_cumulative_production_in_the_gas_phase(self,
                                                   molar_mass_carbon: float,
                                                   dry_mass_sample: float,
                                                   ):
        # oxygen cumulative consumed
        CumulativeProductionGasPhase.cumulative_operation(
            data_frame=self.data_frame,
            name_column_cum=self.create_name_column_oxygen_consumed_cumulative,
            name_column_produced_or_consumed=self.create_name_column_oxygen_consumed,
            name_column_flush=self.get_name_column_flush)
        # carbon dioxide cumulative consumed
        CumulativeProductionGasPhase.cumulative_operation(
            data_frame=self.data_frame,
            name_column_cum=self.create_name_column_C_dioxide_produced_cumulative,
            name_column_produced_or_consumed=self.create_name_name_column_carbon_dioxide_produced,
            name_column_flush=self.get_name_column_flush)
        # total carbon cumulative consumed
        CumulativeProductionGasPhase.cumulative_operation(
            data_frame=self.data_frame,
            name_column_cum=self.create_name_column_C_total_produced_cumulative,
            name_column_produced_or_consumed=self.create_name_column_mCTot_produced,
            name_column_flush=self.get_name_column_flush)

        # total carbon gas dry mass cumulative
        CumulativeProductionGasPhase.carbon_gas_dry_mass_cumulative(
            data_frame=self.data_frame,
            name_column=self.create_name_column_C_gas_dry_mass_cumulative,
            name_column_mCTot_produced_cumulative=self.create_name_column_C_total_produced_cumulative,
            molar_mass_carbon=molar_mass_carbon,
            dry_mass_sample=dry_mass_sample,
            name_column_flush=self.get_name_column_flush)

    def run_carbon_in_aqueous_phase(self,
                                    water_volume_in_liters: float,
                                    dry_mass_sample: float
                                    ):
        # before sampling
        CarbonInAqueousPhase.partial_pressure_carbon_dioxide(
            data_frame=self.data_frame,
            name_column=self.create_name_column_PP_CO2_bs,
            column_name_pressure_sampling=self.get_column_name_pressure_before,
            column_name_corrected_carbon_dioxide_in_percentage=self.create_name_correction_co2
        )
        CarbonInAqueousPhase.carbon_dioxide_in_aqueous_phase_mol_per_m3(
            data_frame=self.data_frame,
            name_column=self.create_name_column_CO2_before_aq_mol_per_m3,
            column_name_PP_CO2=self.create_name_column_PP_CO2_bs
        )
        CarbonInAqueousPhase.carbon_dioxide_in_aqueous_phase_mol(
            data_frame=self.data_frame,
            name_column=self.create_name_column_CO2_before_aq_mol,
            column_name_CO2_aq_in_mol_per_m3=self.create_name_column_CO2_before_aq_mol_per_m3,
            water_volume_in_liters=water_volume_in_liters
        )

        # after sampling
        CarbonInAqueousPhase.partial_pressure_carbon_dioxide(
            data_frame=self.data_frame,
            name_column=self.create_name_column_PP_CO2_as,
            column_name_pressure_sampling=self.get_column_name_pressure_after,
            column_name_corrected_carbon_dioxide_in_percentage=self.create_name_correction_co2)

        CarbonInAqueousPhase.carbon_dioxide_in_aqueous_phase_mol_per_m3(
            data_frame=self.data_frame,
            name_column=self.create_name_column_CO2_after_aq_mol_per_m3,
            column_name_PP_CO2=self.create_name_column_PP_CO2_as)

        CarbonInAqueousPhase.carbon_dioxide_in_aqueous_phase_mol(data_frame=self.data_frame,
                                                                 name_column=self.create_name_column_CO2_after_aq_mol,
                                                                 column_name_CO2_aq_in_mol_per_m3=
                                                                 self.create_name_column_CO2_after_aq_mol_per_m3,
                                                                 water_volume_in_liters=water_volume_in_liters)

        # CO2 dissolved between times steps aqueous
        CarbonInAqueousPhase.carbon_dioxide_dissolved_between_time_steps_aqueous(
            data_frame=self.data_frame,
            name_column=self.create_name_column_CO2_dissolved_between_time_steps_aq,
            column_name_CO2_before_aq_in_mol=self.create_name_column_CO2_before_aq_mol,
            column_name_CO2_after_aq_in_mol=self.create_name_column_CO2_after_aq_mol
        )

        # other
        CarbonInAqueousPhase.carbon_dioxide_produced_aqueous_phase_cumulative(
            data_frame=self.data_frame,
            name_column=self.create_name_column_CO2_produced_aq_cum,
            carbon_dioxide_dissolved_between_time_steps_aqueous=
            self.create_name_column_CO2_dissolved_between_time_steps_aq
        )
        CarbonInAqueousPhase.dissolved_inorganic_carbon_cumulative(
            data_frame=self.data_frame,
            name_column=self.create_name_column_DIC_cum,
            column_name_CO2_aq_in_mol_per_m3=self.create_name_column_CO2_produced_aq_cum,
            dry_mass_sample=dry_mass_sample,
        )

    def run_results_Interpretations(self,):
        ResultsInterpretations.total_carbon_dry_matter(
            data_frame=self.data_frame,
            name_column=self.create_name_column_Ctot_DM,
            name_column_flush=self.get_name_column_flush,
            name_column_C_gas_dry_mass_cum=
            self.create_name_column_C_gas_dry_mass_cumulative,
            name_column_DIC_cum=self.create_name_column_DIC_cum,
        )

        ResultsInterpretations.ratio_oxygen_consumed_carbon_dioxide_produced(
            data_frame=self.data_frame,
            name_column=self.create_name_column_ratio_O2_CO2,
            name_column_O2_consumed_mol=self.create_name_column_oxygen_consumed,
            name_column_CO2_produced_gas_mol=self.create_name_name_column_carbon_dioxide_produced,
            carbon_dioxide_dissolved_between_time_steps_aqueous=
            self.create_name_column_CO2_dissolved_between_time_steps_aq,
            name_column_flush=self.get_name_column_flush
        )
