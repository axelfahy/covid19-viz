# -*- coding: utf-8 -*-
"""Plot functions for covid-19."""
from typing import Dict, Optional, Tuple
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def plot_countries_evolution(data: Dict[str, pd.DataFrame],
                             df_country: pd.DataFrame,
                             *countries,
                             cases: str = 'Confirmed',
                             relatif: bool = False,
                             ax: Optional[plt.axes] = None,
                             figsize: Tuple[int, int] = (16, 8),
                             dpi: int = 80,
                             **kwargs) -> plt.axes:
    """
    Plot the evolution of covid19 for the given countries.

    Parameters
    ----------
    data : dict
        Dictionnary with the data, value must be the DataFrame containing the timeseries.
    df_country : pd.DataFrame
        DataFrame with the country population size.
    *countries
        Positional arguments containing the countries to plot.
    cases : str, default 'Confirmed'
        Key of the dictionary `data` to process.
    relatif : bool, default False
        If True, don't plot the point before the first case of covid for each country.
    ax : plt.axes, optional
        Axes from matplotlib, if None, new figure and axes will be created.
    figsize : Tuple[int, int], default (13, 10)
        Size of the figure to plot.
    dpi : int, default 80
        Resolution of the figure.
    **kwargs
        Additional keyword arguments to be passed to the
        `plt.plot` function from matplotlib.

    Returns
    -------
    plt.axes
        Axes returned by the `plt.subplots` function.
    """
    # Check the countries
    countries = [country for country in countries
                 if country in df_country.index and
                 country in data[cases].index.get_level_values(1)]
    assert len(countries) != 0, 'No country to process'

    if ax is None:
        _, ax = plt.subplots(1, 1, figsize=figsize, dpi=dpi)

    colors = iter(plt.cm.rainbow(np.linspace(0, 1, len(countries))))

    for country in countries:
        df_plot = data[cases].query('Country == @country').groupby('Country').sum()
        if relatif:
            df_plot = df_plot.loc[:, (df_plot != 0).any(axis='index')]

        ax.plot(df_plot.values.T / int(
            df_country.query('Country == @country')['Population'][0].replace(',', '')),
                label=country, marker='o', color=next(colors), **kwargs)

    ax.set_title(f'Evolution of covid19 by country ({cases.lower()})', fontsize=14)
    ax.set_xlabel(f'Number of days since first case{" in country" if relatif else ""}',
                  fontsize=12)
    ax.set_ylabel("Cases / Population's size", fontsize=12)
    ax.legend(loc='upper left')

    # Set horizontal grid.
    ax.grid(axis='y', alpha=0.4, linestyle='-.')

    # Style.
    # Remove border on the top and right.
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    # Set alpha on remaining borders.
    ax.spines['left'].set_alpha(0.4)
    ax.spines['bottom'].set_alpha(0.4)
    # Only show ticks on the left and bottom spines.
    ax.yaxis.set_ticks_position('none')
    ax.xaxis.set_ticks_position('none')

    return ax
