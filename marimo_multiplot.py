import marimo

__generated_with = "0.23.3"
app = marimo.App()


@app.cell
def _():
    import marimo as mo
    import pandas as pd
    import pvlib
    import warnings

    return mo, pd, pvlib, warnings


@app.cell
def _(mo):
    mo.md("""
    # BSRN Data Explorer

    Download irradiance data from the [Baseline Surface Radiation Network (BSRN)](https://bsrn.awi.de/)
    FTP server and visualize it using `solarpy`.

    > **Credentials**: A free FTP account can be requested via the
    > [BSRN data release guidelines](https://bsrn.awi.de/data/data-release-guidelines/) page.
    """)
    return


@app.cell
def _(mo):
    import plotly.graph_objects as go

    BSRN_STATIONS = [
        ("ale", "Alert, Nunavut",              "Canada",      82.50,  -62.33),
        ("asp", "Alice Springs",               "Australia",  -23.80,  133.89),
        ("bar", "Barrow",                      "USA",         71.32, -156.61),
        ("ber", "Bermuda",                     "UK",          32.27,  -64.67),
        ("bnd", "Bondville",                   "USA",         40.05,  -88.37),
        ("brb", "Brasilia",                    "Brazil",     -15.60,  -47.71),
        ("cab", "Cabauw",                      "Netherlands", 51.97,    4.93),
        ("cam", "Camborne",                    "UK",          50.22,   -5.32),
        ("car", "Carpentras",                  "France",      44.08,    5.06),
        ("cnr", "Cener",                       "Spain",       42.82,   -1.60),
        ("coc", "Cocos Island",                "Australia",  -12.19,   96.84),
        ("cor", "Coronel Fontana",             "Argentina",  -31.52,  -65.45),
        ("dar", "Darwin",                      "Australia",  -12.42,  130.89),
        ("dra", "Desert Rock",                 "USA",         36.63, -116.02),
        ("ele", "El Arenosillo",               "Spain",       37.10,   -6.73),
        ("esc", "Escudero",                    "Chile",      -62.21,  -58.96),
        ("eta", "Eureka",                      "Canada",      80.00,  -85.93),
        ("fpk", "Fort Peck",                   "USA",         48.31, -105.10),
        ("geo", "Georg von Neumayer",          "Germany",    -70.65,   -8.25),
        ("gob", "Gobabeb",                     "Namibia",    -23.56,   15.05),
        ("goo", "Goodwin Creek",               "USA",         34.25,  -89.87),
        ("gwn", "Graciosa",                    "Portugal",    39.09,  -28.03),
        ("her", "Hermanus",                    "South Africa",-34.42,  19.22),
        ("iza", "Izana",                       "Spain",       28.31,  -16.50),
        ("kjp", "Kjeller",                     "Norway",      59.98,   11.04),
        ("lau", "Lauder",                      "New Zealand",-45.04,  169.68),
        ("lin", "Lindenberg",                  "Germany",     52.21,   14.12),
        ("man", "Manaus",                      "Brazil",      -2.89,  -59.97),
        ("mkn", "Mt. Kenya",                   "Kenya",       -0.06,   37.30),
        ("nya", "Ny-Ålesund",                  "Norway",      78.93,   11.93),
        ("pay", "Payerne",                     "Switzerland", 46.82,    6.94),
        ("pda", "Presidente Eduardo Frei",     "Chile",      -62.19,  -58.99),
        ("reg", "Regina",                      "Canada",      50.21, -104.71),
        ("rpb", "Ragged Point Barbados",       "Barbados",    13.17,  -59.43),
        ("sag", "Sagres",                      "Portugal",    37.02,   -8.94),
        ("sap", "Sapporo",                     "Japan",       43.06,  141.33),
        ("sgp", "Southern Great Plains",       "USA",         36.61,  -97.49),
        ("sin", "Singapore",                   "Singapore",    1.30,  103.77),
        ("spo", "South Pole",                  "USA",        -90.00,    0.00),
        ("sum", "Summit Station",              "Greenland",   72.58,  -38.48),
        ("tam", "Tamanrasset",                 "Algeria",     22.79,    5.53),
        ("tav", "Tavor",                       "Israel",      32.68,   35.43),
        ("tir", "Tirunelveli",                 "India",        8.68,   77.80),
        ("tok", "Tokai",                       "Japan",       36.47,  140.61),
        ("tor", "Toravere",                    "Estonia",     58.27,   26.46),
        ("tri", "Trieste",                     "Italy",       45.65,   13.76),
        ("uss", "Ussurijsk",                   "Russia",      43.70,  131.98),
        ("wlo", "Whyalla",                     "Australia",  -33.04,  137.53),
        ("xia", "Xianghe",                     "China",       39.75,  116.96),
    ]

    _abbrs   = [s[0] for s in BSRN_STATIONS]
    _names   = [s[1] for s in BSRN_STATIONS]
    _countries = [s[2] for s in BSRN_STATIONS]
    _lats    = [s[3] for s in BSRN_STATIONS]
    _lons    = [s[4] for s in BSRN_STATIONS]
    _labels  = [f"{a.upper()} — {n} ({c})" for a, n, c in zip(_abbrs, _names, _countries)]

    _fig = go.Figure(go.Scattergeo(
        lat=_lats,
        lon=_lons,
        text=_labels,
        customdata=_abbrs,
        mode="markers",
        marker=dict(
            size=9,
            color="steelblue",
            line=dict(width=0.8, color="white"),
            opacity=0.85,
        ),
        hovertemplate="%{text}<extra></extra>",
        selected=dict(marker=dict(color="orangered", size=13)),
        unselected=dict(marker=dict(opacity=0.4)),
    ))

    _fig.update_layout(
        title=dict(text="Click a station to select it", x=0.5),
        geo=dict(
            showland=True,
            landcolor="#e8e8e8",
            showocean=True,
            oceancolor="#cce5f0",
            showlakes=True,
            lakecolor="#cce5f0",
            showcountries=True,
            countrycolor="#aaaaaa",
            showframe=False,
            projection_type="natural earth",
        ),
        margin=dict(l=0, r=0, t=40, b=0),
        height=470,
        clickmode="event+select",
        dragmode="pan",
        modebar_remove=["select2d", "lasso2d"],
    )

    station_map = mo.ui.plotly(_fig)
    station_map
    return BSRN_STATIONS, station_map


@app.cell
def _(BSRN_STATIONS, mo, station_map):
    _points = station_map.value if isinstance(station_map.value, list) else []
    if _points:
        _idx = _points[0].get("pointIndex", _points[0].get("pointNumber", 0))
        _abbr = BSRN_STATIONS[_idx][0]
    else:
        _abbr = "cab"

    _info = next(s for s in BSRN_STATIONS if s[0] == _abbr)
    selected_station = _abbr

    mo.callout(
        mo.md(f"**Selected:** {_abbr.upper()} — {_info[1]}, {_info[2]}  "
              f"&nbsp;({_info[3]:.2f}°, {_info[4]:.2f}°)"),
        kind="info",
    )
    return (selected_station,)


@app.cell
def _(BSRN_STATIONS, mo, pd):
    import unicodedata

    def _norm(s):
        s = unicodedata.normalize("NFKD", str(s).lower().strip())
        return s.encode("ascii", "ignore").decode()

    # Pangaea portal uses different 3-letter codes for some stations.
    # This maps pangaea_code → pvlib FTP code for the known mismatches.
    _PANGAEA_TO_FTP = {
        "bon": "bnd",  # Bondville
        "eur": "eta",  # Eureka, Canada
        "fpe": "fpk",  # Fort Peck
        "gvn": "geo",  # Georg von Neumayer
        "gcr": "goo",  # Goodwin Creek
        "e13": "sgp",  # Southern Great Plains
        "sgp": "sgp",  # Southern Great Plains (alternate pangaea code)
    }
    _ftp_codes = {s[0] for s in BSRN_STATIONS}
    _name_to_ftp = {_norm(s[1]): s[0] for s in BSRN_STATIONS}

    with mo.status.spinner(title="Loading BSRN data availability…"):
        try:
            _df = pd.read_html("https://dataportals.pangaea.de/bsrn/?q=LR0100")[0]
        except Exception:
            _df = None

    station_years = {}
    if _df is not None:
        _year_cols = sorted(
            int(str(c)) for c in _df.columns
            if str(c).strip().isdigit() and 1990 <= int(str(c).strip()) <= 2030
        )
        _code_col = _df.columns[0]
        _name_col = _df.columns[1] if len(_df.columns) > 1 else None

        for _, _row in _df.iterrows():
            _pcode = str(_row[_code_col]).strip().lower()
            _pname = _norm(_row[_name_col]) if _name_col is not None else ""
            _years = sorted(
                y for y in _year_cols
                if pd.notna(_row.get(y)) and str(_row.get(y, "")).strip() not in ("", "-", "nan")
            )
            if not _years:
                continue
            # Resolve pangaea code → FTP code
            _ftp = _PANGAEA_TO_FTP.get(_pcode)
            if _ftp is None:
                if _pcode in _ftp_codes:
                    _ftp = _pcode
                else:
                    # Fall back to name substring matching
                    for _known_norm, _known_ftp in _name_to_ftp.items():
                        if _known_norm in _pname or _pname in _known_norm:
                            _ftp = _known_ftp
                            break
            if _ftp:
                station_years[_ftp] = _years
    return (station_years,)


@app.cell
def _(mo, selected_station, station_years):
    _available = station_years.get(selected_station, list(range(1992, 2026)))
    if not _available:
        _available = list(range(1992, 2026))
    _default = str(max(_available))

    year_dropdown = mo.ui.dropdown(
        options={str(y): y for y in sorted(_available, reverse=True)},
        value=_default,
        label="Year",
    )

    year_dropdown
    return (year_dropdown,)


@app.cell
def _(mo):
    username_input = mo.ui.text(
        value="",
        label="BSRN FTP username",
        full_width=True,
    )
    password_input = mo.ui.text(
        value="",
        label="BSRN FTP password",
        full_width=True,
    )

    mo.hstack([username_input, password_input], gap=2)
    return password_input, username_input


@app.cell
def _(mo):
    download_button = mo.ui.run_button(label="⬇ Download & Plot", kind="success")

    download_button
    return (download_button,)


@app.cell
def _(download_button, mo):
    mo.stop(
        not download_button.value,
        mo.md("*Configure the options above and click **Download & Plot**.*"),
    )
    return


@app.cell
def _(
    mo,
    password_input,
    pd,
    pvlib,
    selected_station,
    username_input,
    warnings,
    year_dropdown,
):

    _station = selected_station
    _year = int(year_dropdown.value)
    _username = username_input.value.strip()
    _password = password_input.value.strip()

    if not _username or not _password:
        mo.stop(
            True,
            mo.callout(
                mo.md("**Missing credentials** — please enter your BSRN FTP username and password."),
                kind="warn",
            ),
        )

    with mo.status.spinner(title=f"Downloading {_station.upper()} data for {_year}…"):
        try:
            with warnings.catch_warnings(record=True) as _caught:
                warnings.simplefilter("always")
                bsrn_data, bsrn_meta = pvlib.iotools.get_bsrn(
                    station=_station,
                    start=pd.Timestamp(_year, 1, 1),
                    end=pd.Timestamp(_year, 12, 31),
                    username=_username,
                    password=_password,
                )
        except KeyError as _e:
            mo.stop(
                True,
                mo.callout(
                    mo.md(f"**Station not found**: `{_station}` does not exist on the FTP server.\n\n`{_e}`"),
                    kind="danger",
                ),
            )
        except Exception as _e:
            mo.stop(
                True,
                mo.callout(mo.md(f"**Download failed**: {_e}"), kind="danger"),
            )

    if bsrn_data.empty:
        _msgs = "\n\n".join(str(w.message) for w in _caught) or "No data returned."
        mo.stop(
            True,
            mo.callout(
                mo.md(f"**No data available** for `{_station.upper()}` in {_year}.\n\n{_msgs}"),
                kind="warn",
            ),
        )

    mo.callout(
        mo.md(f"✅ Downloaded **{len(bsrn_data):,} rows** for `{_station.upper()}` in {_year}."),
        kind="success",
    )
    return bsrn_data, bsrn_meta


@app.cell
def _(bsrn_data, bsrn_meta, mo, pvlib, selected_station, warnings):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import sys
    import subprocess

    try:
        from solarpy.plotting import multiplot
        from solarpy.processing import resample_to_freq
    except ImportError:
        subprocess.run(
            [sys.executable, "-m", "pip", "install",
             "git+https://github.com/AssessingSolar/solarpy.git", "-q"],
            check=True,
        )
        from solarpy.plotting import multiplot
        from solarpy.processing import resample_to_freq

    _lat = bsrn_meta.get("latitude")
    _lon = bsrn_meta.get("longitude")
    _alt = bsrn_meta.get("altitude", 0)

    if _lat is None or _lon is None:
        mo.stop(
            True,
            mo.callout(
                mo.md(f"**Could not find lat/lon in metadata.**\n\nAvailable keys: `{list(bsrn_meta.keys())}`"),
                kind="danger",
            ),
        )

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        _solpos = pvlib.solarposition.get_solarposition(
            bsrn_data.index, _lat, _lon, altitude=_alt
        )

    _plot_data = bsrn_data[["ghi", "dni", "dhi"]].copy()
    _plot_data["solar_zenith"] = _solpos["apparent_zenith"].values
    _plot_data["solar_azimuth"] = _solpos["azimuth"].values
    _plot_data = resample_to_freq(_plot_data, freq="1min")

    _meta = {
        "latitude": _lat,
        "longitude": _lon,
        "altitude": _alt,
        "name": bsrn_meta.get("station name", selected_station.upper()),
        "country": bsrn_meta.get("country", ""),
        "climate": bsrn_meta.get("climate zone", ""),
    }

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        _fig, _axes = multiplot(
            times=_plot_data.index,
            data=_plot_data,
            meta=_meta,
            figsize=(24, 16),
        )

    plt.tight_layout()
    _fig
    return


@app.cell
def _():
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
