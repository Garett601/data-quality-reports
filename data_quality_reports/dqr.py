"""Class to create Data Quality Reports."""

import numpy as np
import pandas as pd


class DQR:
    """A class used to perform a data quality report (DQR) on a DataFrame.

    Attributes
    ----------
    df : pd.DataFrame
        The DataFrame to analyze.
    data_types : pd.DataFrame
        DataFrame containing information about data types of the input DataFrame's columns.
    continuous_data : pd.DataFrame
        DataFrame containing continuous data.
    categorical_data : pd.DataFrame
        DataFrame containing categorical data.

    Methods
    -------
    _get_data_types()
        Retrieves the data types for the DataFrame columns.
    _create_continuous_df()
        Creates a DataFrame with continuous data.
    _create_categorical_df()
        Creates a DataFrame with categorical data.
    _update_continuous_df(continuous_data)
        Updates the continuous_data DataFrame with statistical information.
    _update_categorical_df(categorical_data)
        Updates the categorical_data DataFrame with mode, mode frequency, and percentage.
    get_continuous_df()
        Returns the DataFrame containing continuous data.
    get_categorical_df()
        Returns the DataFrame containing categorical data.
    write_to_csv()
        Writes the continuous and categorical data DataFrames to CSV files.
    """

    CONTINUOUS_DEFAULT_PATH = "continuous_data.csv"
    CATEGORICAL_DEFAULT_PATH = "categorical_data.csv"

    def __init__(self, df: pd.DataFrame) -> None:
        """Initialise DQR instance.

        Parameters
        ----------
        df : pd.DataFrame
            DataFrame for which reports will be generated.
        """
        self.df = df
        self.data_types = self._get_data_types()
        self.continuous_data = self._create_continuous_df()
        self.categorical_data = self._create_categorical_df()

    def _get_data_types(self) -> pd.DataFrame:
        """Retrieve data types for the DataFrame columns.

        Returns
        -------
        pd.DataFrame
            DataFrame containing information about data types of the input DataFrame's columns.
        """
        data_types = pd.DataFrame(self.df.dtypes, columns=["data_type"])
        data_types["count"] = self.df.count()
        data_types["missing"] = round(((len(self.df) - self.df.count()) / (len(self.df))) * 100, 2)
        card = [self.df[col].nunique() for col in self.df.columns]
        data_types["cardinality"] = card
        data_types.loc[data_types["cardinality"] == 2, "data_type"] = "object"

        return data_types

    def _create_continuous_df(self) -> pd.DataFrame:
        """Create DataFrame with continuous data.

        Returns
        -------
        pd.DataFrame
            DataFrame containing continuous data along with statistical information.
        """
        continuous_data = self.data_types[
            (self.data_types["data_type"] != "object") | (self.data_types["data_type"] == "datetime64[ns]")
        ].copy()

        continuous_data = self._update_continuous_df(continuous_data)
        continuous_data.sort_values("missing", ascending=False, inplace=True)

        return continuous_data

    def _create_categorical_df(self) -> pd.DataFrame:
        """Create DataFrame with categorical data.

        Returns
        -------
        pd.DataFrame
            DataFrame containing categorical data along with mode, mode frequency, and percentage.
        """
        categorical_data = self.data_types[
            (self.data_types["data_type"] == "object") & (self.data_types["data_type"] != "datetime64[ns]")
        ].copy()

        categorical_data = self._update_categorical_df(categorical_data)
        categorical_data.sort_values("missing", ascending=False, inplace=True)

        return categorical_data

    def _update_continuous_df(self, continuous_data: pd.DataFrame) -> pd.DataFrame:
        """Update continuous_data DataFrame with statistical information.

        Parameters
        ----------
        continuous_data : pd.DataFrame
            DataFrame containing continuous data.

        Returns
        -------
        pd.DataFrame
            DataFrame containing continuous data along with statistical information.
        """
        continuous_data["min"] = [
            round(self.df[ind].min(), 2) if continuous_data.loc[ind, "data_type"] != "<M8[ns]" else self.df[ind].min()
            for ind in continuous_data.index
        ]
        continuous_data["1st qrt"] = [
            round(self.df[ind].quantile([0.25]).values[0], 2)
            if continuous_data.loc[ind, "data_type"] != "<M8[ns]"
            else self.df[ind].quantile([0.25]).values[0]
            for ind in continuous_data.index
        ]
        continuous_data["mean"] = [
            round(self.df[ind].mean(), 2)
            if continuous_data.loc[ind, "data_type"] != "<M8[ns]"
            else self.df[ind].mean()
            for ind in continuous_data.index
        ]
        continuous_data["median"] = [
            round(self.df[ind].median(), 2)
            if continuous_data.loc[ind, "data_type"] != "<M8[ns]"
            else self.df[ind].median()
            for ind in continuous_data.index
        ]
        continuous_data["3rd qrt"] = [
            round(self.df[ind].quantile([0.75]).values[0], 2)
            if continuous_data.loc[ind, "data_type"] != "<M8[ns]"
            else self.df[ind].quantile([0.75]).values[0]
            for ind in continuous_data.index
        ]
        continuous_data["max"] = [
            round(self.df[ind].max(), 2) if continuous_data.loc[ind, "data_type"] != "<M8[ns]" else self.df[ind].max()
            for ind in continuous_data.index
        ]
        continuous_data["std dev"] = [
            round(self.df[ind].std(), 2) if continuous_data.loc[ind, "data_type"] != "<M8[ns]" else self.df[ind].std()
            for ind in continuous_data.index
        ]
        return continuous_data

    def _update_categorical_df(self, categorical_data: pd.DataFrame) -> pd.DataFrame:
        """Update categorical_data DataFrame with mode, mode frequency, and percentage.

        Parameters
        ----------
        categorical_data : pd.DataFrame
            DataFrame containing categorical data.

        Returns
        -------
        pd.DataFrame
            DataFrame containing categorical data along with mode, mode frequency, and percentage.
        """
        mode = [self.df[ind].mode().values[0] for ind in categorical_data.index]
        mode_freq = [self.df[ind].value_counts().iloc[0] for ind in categorical_data.index]
        mode_perc = [round((mode_freq[i] / len(self.df) * 100), 2) for i in range(len(mode_freq))]
        mode_2 = [
            self.df[ind].value_counts().index[1] if categorical_data.loc[ind, "cardinality"] > 1 else np.nan
            for ind in categorical_data.index
        ]
        mode_freq_2 = [
            self.df[ind].value_counts().iloc[1] if categorical_data.loc[ind, "cardinality"] > 1 else np.nan
            for ind in categorical_data.index
        ]
        mode_perc_2 = [round((mode_freq_2[i] / len(self.df) * 100), 2) for i in range(len(mode_freq_2))]

        categorical_data["mode"] = mode
        categorical_data["mode_freq"] = mode_freq
        categorical_data["mode_percent"] = mode_perc
        categorical_data["mode_2"] = mode_2
        categorical_data["mode_2_freq"] = mode_freq_2
        categorical_data["mode_2_perc"] = mode_perc_2
        return categorical_data

    def get_continuous_df(self) -> pd.DataFrame:
        """Return DataFrame containing continuous data.

        Returns
        -------
        pd.DataFrame
            DataFrame containing continuous data.
        """
        return self.continuous_data

    def get_categorical_df(self) -> pd.DataFrame:
        """Return DataFrame containing categorical data.

        Returns
        -------
        pd.DataFrame
            DataFrame containing categorical data.
        """
        return self.categorical_data

    def write_to_csv(self, continuous_path: str = "", categorical_path: str = "") -> None:
        """Write continuous and categorical data DataFrames to CSV files.

        Parameters
        ----------
        continuous_path : str, optional
            The path where the continuous data CSV file should be saved.
            Defaults to CONTINUOUS_DEFAULT_PATH if not provided.
        categorical_path : str, optional
            The path where the categorical data CSV file should be saved.
            Defaults to CATEGORICAL_DEFAULT_PATH if not provided.

        Returns
        -------
        None
        """
        continuous_path = continuous_path or self.CONTINUOUS_DEFAULT_PATH
        categorical_path = categorical_path or self.CATEGORICAL_DEFAULT_PATH

        self.continuous_data.to_csv(continuous_path)
        self.categorical_data.to_csv(categorical_path)
