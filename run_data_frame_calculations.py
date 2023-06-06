from data_frame_processor import DataFrameProcessor
from standard_gas_composition_calculations import GasComposition, PercentageO2ConsumedAndCO2ProducedAndRatio, \
    MolGasCompositionCalculations, MolesProduced, CumulativeProductionGasPhase, CarbonInAqueousPhase, \
    ResultsInterpretations
import pandas as pd


class RunDataFrameCalculationsForOneDataFrame:
    """"run the calculations on the data frame"""
    data_frame: object

    def __init__(self, data_frame):
        self.data_frame = data_frame

    def run_data_frame_processor_calculations(self, fraction_to_time: bool = False):
        DataFrameProcessor.fill_nan_values(data_frame=self.data_frame, column_name="Time", value="00:00:00")
        DataFrameProcessor.add_day_column(data_frame=self.data_frame, date_column_name="Date", time_column_name="Time",
                                          fraction_to_time=fraction_to_time)

    def run_gas_composition_calculations(self):
        GasComposition.set_gas_composition(data_frame=self.data_frame, ch4=0, co2=0.03, o2=21.90, n2=78.07, index=0)
        GasComposition.sum_correct_sum(data_frame=self.data_frame)

    def run_percentage_o2_consumed_and_co2_produced_and_ratio_calculations(self):
        PercentageO2ConsumedAndCO2ProducedAndRatio.calculate_o2_consumed(data_frame=self.data_frame)
        PercentageO2ConsumedAndCO2ProducedAndRatio.calculate_co2_produced(data_frame=self.data_frame)
        PercentageO2ConsumedAndCO2ProducedAndRatio.calculate_ratio_o2_co2(data_frame=self.data_frame)

    def run_mol_gases_before_and_after_sampling(self,
                                                Rgas: float,
                                                exp_temperature: float,
                                                volume_headspace: float,
                                                name_column_mg_bs: str = "mg_bs",
                                                name_column_mg_as: str = "mg_as",
                                                column_name_pressure_before: str = "P sample before gc [hPa]",
                                                column_name_pressure_after: str = "P sample after gc [hPa]",
                                                ):
        # moles gas before sampling
        MolGasCompositionCalculations.mol_gas_sampling(data_frame=self.data_frame,
                                                       Rgas=Rgas,
                                                       exp_temperature=exp_temperature,
                                                       volume_headspace=volume_headspace,
                                                       column_name_pressure=column_name_pressure_before,
                                                       name_column=name_column_mg_bs
                                                       )

        # moles gas after sampling
        MolGasCompositionCalculations.mol_gas_sampling(data_frame=self.data_frame,
                                                       Rgas=Rgas,
                                                       exp_temperature=exp_temperature,
                                                       volume_headspace=volume_headspace,
                                                       column_name_pressure=column_name_pressure_after,
                                                       name_column=name_column_mg_as
                                                       )

    def run_mol_gas_composition_calculation(self,
                                            name_column_mg_bs: str = "mg_bs",
                                            name_column_mg_as: str = "mg_as",
                                            name_column_mCO2_b: str = "mCO2_b",
                                            name_column_mCH4_b: str = "mCH4_b",
                                            name_column_mO2_b: str = "mO2_b",
                                            name_column_mN2_b: str = "mN2_b",
                                            name_corr_CO2: str = "CO2-corr [%]",
                                            name_corr_CH4: str = "CH4-corr [%]",
                                            name_corr_O2: str = "O2-corr [%]",
                                            name_corr_N2: str = "N2-corr [%]",
                                            name_column_mCO2_a: str = "mCO2_a",
                                            name_column_mCH4_a: str = "mCH4_a",
                                            name_column_mO2_a: str = "mO2_a",
                                            name_column_mN2_a: str = "mN2_a",
                                            name_column_CTot_b: str = "mCTot_b",
                                            name_column_cTot_a: str = "mCTot_a"
                                            ):
        # CO2 before
        MolGasCompositionCalculations.specific_gas_in_moles_before_sampling(data_frame=self.data_frame,
                                                                            name_column=name_column_mCO2_b,
                                                                            name_column_mg_before_or_after=
                                                                            name_column_mg_bs,
                                                                            name_column_specific_gas_corrected=
                                                                            name_corr_CO2)
        # CH4 before
        MolGasCompositionCalculations.specific_gas_in_moles_before_sampling(data_frame=self.data_frame,
                                                                            name_column=name_column_mCH4_b,
                                                                            name_column_mg_before_or_after=
                                                                            name_column_mg_bs,
                                                                            name_column_specific_gas_corrected=
                                                                            name_corr_CH4)
        # O2 before
        MolGasCompositionCalculations.specific_gas_in_moles_before_sampling(data_frame=self.data_frame,
                                                                            name_column=name_column_mO2_b,
                                                                            name_column_mg_before_or_after=
                                                                            name_column_mg_bs,
                                                                            name_column_specific_gas_corrected=
                                                                            name_corr_O2)
        # N2 before
        MolGasCompositionCalculations.specific_gas_in_moles_before_sampling(data_frame=self.data_frame,
                                                                            name_column=name_column_mN2_b,
                                                                            name_column_mg_before_or_after=
                                                                            name_column_mg_bs,
                                                                            name_column_specific_gas_corrected=
                                                                            name_corr_N2)
        # total carbon before
        MolGasCompositionCalculations.carbon_total_moles(data_frame=self.data_frame, name_column=name_column_CTot_b,
                                                         name_column_CO2=name_column_mCO2_b,
                                                         name_column_CH4=name_column_mCH4_b)

        # CO2 after
        MolGasCompositionCalculations.specific_gas_in_moles_before_sampling(data_frame=self.data_frame,
                                                                            name_column=name_column_mCO2_a,
                                                                            name_column_mg_before_or_after=
                                                                            name_column_mg_as,
                                                                            name_column_specific_gas_corrected=
                                                                            name_corr_CO2)
        # CH4 after
        MolGasCompositionCalculations.specific_gas_in_moles_before_sampling(data_frame=self.data_frame,
                                                                            name_column=name_column_mCH4_a,
                                                                            name_column_mg_before_or_after=
                                                                            name_column_mg_as,
                                                                            name_column_specific_gas_corrected=
                                                                            name_corr_CH4)
        # O2 after
        MolGasCompositionCalculations.specific_gas_in_moles_before_sampling(data_frame=self.data_frame,
                                                                            name_column=name_column_mO2_a,
                                                                            name_column_mg_before_or_after=
                                                                            name_column_mg_as,
                                                                            name_column_specific_gas_corrected=
                                                                            name_corr_O2)
        # N2 after
        MolGasCompositionCalculations.specific_gas_in_moles_before_sampling(data_frame=self.data_frame,
                                                                            name_column=name_column_mN2_a,
                                                                            name_column_mg_before_or_after=
                                                                            name_column_mg_as,
                                                                            name_column_specific_gas_corrected=
                                                                            name_corr_N2)
        # total carbon before
        MolGasCompositionCalculations.carbon_total_moles(data_frame=self.data_frame, name_column=name_column_cTot_a,
                                                         name_column_CO2=name_column_mCO2_a,
                                                         name_column_CH4=name_column_mCH4_a)

    def run_moles_produced(self,
                           name_column_mCTot_produced: str = "mCTot_produced",
                           name_column_mCTot_b: str = "mCTot_b",
                           name_column_mCTot_a: str = "mCTot_a",
                           name_column_oxygen_consumed: str = "O2 consumed",
                           name_column_O2_before: str = "mO2_b",
                           name_column_O2_after: str = "mO2_a",
                           name_column_carbon_dioxide_produced: str = "CO2 produced",
                           name_column_CO2_before: str = "mCO2_b",
                           name_column_CO2_after: str = "mCO2_a",
                           name_column_flush: str = "Flush (1=yes; 0=no)"):
        MolesProduced.total_carbon_produced_moles(data_frame=self.data_frame,
                                                  name_column=name_column_mCTot_produced,
                                                  name_column_mCTot_b=name_column_mCTot_b,
                                                  name_column_mCTot_a=name_column_mCTot_a,
                                                  name_column_flush=name_column_flush
                                                  )
        MolesProduced.oxygen_consumed_moles(data_frame=self.data_frame,
                                            name_column=name_column_oxygen_consumed,
                                            name_column_mO2_b=name_column_O2_before,
                                            name_column_mO2_a=name_column_O2_after,
                                            name_column_flush=name_column_flush
                                            )
        MolesProduced.carbon_dioxide_produced_moles(data_frame=self.data_frame,
                                                    name_column=name_column_carbon_dioxide_produced,
                                                    name_column_mCO2_b=name_column_CO2_before,
                                                    name_column_mCO2_a=name_column_CO2_after,
                                                    name_column_flush=name_column_flush
                                                    )

    def run_cumulative_production_in_the_gas_phase(self,
                                                   molar_mass_carbon: float,
                                                   dry_mass_sample: float,
                                                   name_column_oxygen_consumed_cumulative: str = "O2 consumed_cum",
                                                   name_column_oxygen_consumed: str = "O2 consumed",
                                                   name_column_C_dioxide_produced_cumulative: str = "CO2 produced_cum",
                                                   name_column_C_dioxide_produced: str = "CO2 produced",
                                                   name_column_C_total_produced_cumulative: str = "mCTot_produced_cum",
                                                   name_column_C_total_produced: str = "mCTot_produced",
                                                   name_column_flush: str = "Flush (1=yes; 0=no)",
                                                   name_column_C_gas_dry_mass_cumulative: str = "Cgas_DM_cum ",
                                                   name_column_mCTot_produced_cumulative: str = "mCTot_produced_cum"
                                                   ):
        # oxygen cumulative consumed
        CumulativeProductionGasPhase.cumulative_operation(data_frame=self.data_frame,
                                                          name_column_cum=name_column_oxygen_consumed_cumulative,
                                                          name_column_produced_or_consumed=name_column_oxygen_consumed,
                                                          name_column_flush=name_column_flush)
        # carbon dioxide cumulative consumed
        CumulativeProductionGasPhase.cumulative_operation(data_frame=self.data_frame,
                                                          name_column_cum=name_column_C_dioxide_produced_cumulative,
                                                          name_column_produced_or_consumed=name_column_C_dioxide_produced,
                                                          name_column_flush=name_column_flush)
        # total carbon cumulative consumed
        CumulativeProductionGasPhase.cumulative_operation(data_frame=self.data_frame,
                                                          name_column_cum=name_column_C_total_produced_cumulative,
                                                          name_column_produced_or_consumed=name_column_C_total_produced,
                                                          name_column_flush=name_column_flush)

        # total carbon gas dry mass cumulative
        CumulativeProductionGasPhase.carbon_gas_dry_mass_cumulative(data_frame=self.data_frame,
                                                                    name_column=name_column_C_gas_dry_mass_cumulative,
                                                                    name_column_mCTot_produced_cumulative=
                                                                    name_column_mCTot_produced_cumulative,
                                                                    molar_mass_carbon=molar_mass_carbon,
                                                                    dry_mass_sample=dry_mass_sample,
                                                                    name_column_flush=name_column_flush)

    def run_carbon_in_aqueous_phase(self,
                                    water_volume_in_liters: float,
                                    dry_mass_sample: float,
                                    name_column_PP_CO2_bs: str = "PP CO2_b ",
                                    column_name_pressure_before_sampling: str = "P sample before gc [hPa]",
                                    column_name_corrected_carbon_dioxide_in_percentage: str = "CO2-corr [%]",
                                    name_column_CO2_aq_mol_per_m3: str = "CO2_aq [mol/m3]",
                                    name_column_CO2_aq_mol: str = "CO2_aq [mol]",
                                    name_column_CO2_produced_aq: str = "CO2_produced_aq",
                                    name_column_DIC_cum: str = "DIC_cum",
                                    ):
        CarbonInAqueousPhase.partial_pressure_carbon_dioxide_before_sampling(
            data_frame=self.data_frame,
            name_column=name_column_PP_CO2_bs,
            column_name_pressure_before_sampling=column_name_pressure_before_sampling,
            column_name_corrected_carbon_dioxide_in_percentage=column_name_corrected_carbon_dioxide_in_percentage
        )
        CarbonInAqueousPhase.carbon_dioxide_in_aqueous_phase_mol_per_m3(
            data_frame=self.data_frame,
            name_column=name_column_CO2_aq_mol_per_m3,
            column_name_PP_CO2_bs=name_column_PP_CO2_bs
        )
        CarbonInAqueousPhase.carbon_dioxide_in_aqueous_phase_mol(
            data_frame=self.data_frame,
            name_column=name_column_CO2_aq_mol,
            column_name_CO2_aq_in_mol_per_m3=name_column_CO2_aq_mol_per_m3,
            water_volume_in_liters=water_volume_in_liters
        )
        CarbonInAqueousPhase.carbon_dioxide_produced_aqueous_phase(
            data_frame=self.data_frame,
            name_column=name_column_CO2_produced_aq,
            column_name_CO2_aq_in_mol=name_column_CO2_aq_mol,
        )
        CarbonInAqueousPhase.dissolved_inorganic_carbon_cumulative(
            data_frame=self.data_frame,
            name_column=name_column_DIC_cum,
            column_name_CO2_aq_in_mol_per_m3=name_column_CO2_aq_mol_per_m3,
            dry_mass_sample=dry_mass_sample,
            water_volume_in_liters=water_volume_in_liters,
        )

    def run_results_Interpretations(self,
                                    name_column_Ctot_DM: str = "Ctot_DM [mg C/gDW]",
                                    name_column_ratio_O2_CO2: str = "Ratio O2/CO2",
                                    name_column_flush: str = "Flush (1=yes; 0=no)",
                                    name_column_C_gas_dry_mass_cumulative: str = "Cgas_DM_cum ",
                                    name_column_DIC_cum: str = "DIC_cum",
                                    name_column_oxygen_consumed: str = "O2 consumed",
                                    name_column_C_dioxide_produced: str = "CO2 produced",
                                    name_column_CO2_produced_aq: str = "CO2_produced_aq",
                                    ):
        ResultsInterpretations.total_carbon_dry_matter(
            data_frame=self.data_frame,
            name_column=name_column_Ctot_DM,
            name_column_flush=name_column_flush,
            name_column_C_gas_dry_mass_cum=
            name_column_C_gas_dry_mass_cumulative,
            name_column_DIC_cum=name_column_DIC_cum,
        )

        ResultsInterpretations.ratio_oxygen_consumed_carbon_dioxide_produced(
            data_frame=self.data_frame,
            name_column=name_column_ratio_O2_CO2,
            name_column_O2_consumed_mol=name_column_oxygen_consumed,
            name_column_CO2_produced_mol=name_column_C_dioxide_produced,
            name_column_CO2_produced_aqueous_mol=name_column_CO2_produced_aq,
            name_column_flush=name_column_flush
        )
