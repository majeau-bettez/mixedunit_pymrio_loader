from pathlib import Path
import pandas as pd
import pyxlsb
import pymrio

# Filenames
file_mr_final_demand = 'MR_HFD_2011_v3_3_17'
file_economic_system = 'Exiobase_MR_HIOT_2011_v3_3_17_by_prod_tech'
file_extensions = 'MR_HIOT_2011_v3_3_17_extensions'


def load_pxp_io(path, extension_category = 'Emiss', version='3.3.17', file_format='xlsb'):
    """ Loads the mixed-unit Exiobase IO into a pyMRIO object

    Args
    ----

    path : str
        Location of the directory
    extension_category: str
        Name of the environmental extension that we seek
    version: str
        So far, this loader is only specified for version 3.3.17
    file_format: str ['xlsb' (default) | 'xlsx']
        Read file as binary spreadsheet (requires `pyxlsb` installed), or as OfficeOpen XML spreadsheet

    Returns
    -------

    io: pymrio object
        The IO system

    """

    path = Path(path)

    if file_format == 'xlsb':
        ext = '.' + file_format
        engine = 'pyxlsb'
    elif file_format == 'xlsx':
        ext = '.' + file_format
        engine = None

    # Read economic system
    fullpath = Path(path, file_economic_system).with_suffix(ext)
    with pd.ExcelFile( fullpath, engine=engine) as f:
        # Read in final demand
        Y = pd.read_excel(f, sheet_name='FD', index_col=[0,1,2,3,4], header=[0,1,2,3])

        # Read in economic exchanges
        Z = pd.read_excel(f, sheet_name='HIOT', index_col=[0,1, 2, 3, 4], header=[0, 1, 2, 3])


    # Read environmental extensions
    fullpath = Path(path, file_extensions).with_suffix(ext)
    with pd.ExcelFile(fullpath, engine=engine) as f:

        # Read in total sectoral exchanges with the environment
        sheet_name = extension_category + '_act'
        F = pd.read_excel(f, sheet_name=sheet_name, header=[0,1,2,3], index_col=[0,2,1])

        # Read household exchanges with the environment
        sheet_name = extension_category + '_FD'
        FY = pd.read_excel(f, sheet_name=sheet_name, header=[0,1,2,3], index_col=[0,2,1])



    # Fix columns of final demand - bug in 3.3.17 export
    Y = Y.iloc(axis=1)[:FY.columns.shape[0]]
    Y.columns = FY.columns


    # Put Units where they belong
    commodity_units = Y.reset_index(level=-1).iloc(axis=1)[0]
    Y.index = Y.index.droplevel(-1)
    Z.index = Z.index.droplevel(-1)

    # Same treatment of units for environmental extensions
    factor_units = F.reset_index(-1).iloc(axis=1)[0]
    F.index = F.index.droplevel(-1)
    FY.index = FY.index.droplevel(-1)


    # Use the same labels for rows and columns of Z matrix -- enforce product x product assumption of pymrio
    Z.columns = Z.index
    F.columns = Z.index


    # Put in pymrio
    io = pymrio.IOSystem(Z=Z, Y=Y,unit=commodity_units)
    io.satellite = pymrio.Extension('Satellite Accounts', F=F, F_Y=FY,  unit=factor_units)

    return io

