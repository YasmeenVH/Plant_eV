from analysis.dataloader import DataLoader
import config


def main():
    Loader_DC = DataLoader(path=config.dcbias_results,file_type=config.file_type[0], blue = config.dcbias_blue, red = config.dcbias_red, amber= config.dcbias_amber, res= True, n_points = config.n_points)
    bluedc_file_names = Loader_DC.read_files(Loader_DC.blue + '/'+ Loader_DC.r1, Loader_DC.n_points)


    ### Loading all HDF5 of official results to perform analysis
    Loader_HDF5_1 = DataLoader(path=config.path_official_results,file_type=config.file_type[1], blue = config.official_blue[0], red = config.official_red[0], amber= config.official_amber[0], res= False, n_points = config.n_points)
    blue_official_p1 = Loader_HDF5_1.read_files(Loader_HDF5_1.blue, Loader_DC.n_points)
    red_official_p1 = Loader_HDF5_1.read_files(Loader_HDF5_1.red, Loader_DC.n_points)
    amber_official_p1 = Loader_HDF5_1.read_files(Loader_HDF5_1.amber, Loader_DC.n_points)

    Loader_HDF5_2 = DataLoader(path=config.path_official_results, file_type=config.file_type[1],
                             blue=config.official_blue[1], red=config.official_red[1], amber=config.official_amber[1],
                             res=False, n_points=config.n_points)
    blue_official_p2 = Loader_HDF5_2.read_files(Loader_HDF5_2.blue, Loader_DC.n_points)
    red_official_p2 = Loader_HDF5_2.read_files(Loader_HDF5_2.red, Loader_DC.n_points)
    amber_official_p2 = Loader_HDF5_2.read_files(Loader_HDF5_2.amber, Loader_DC.n_points)

    Loader_HDF5_3 = DataLoader(path=config.path_official_results, file_type=config.file_type[1],
                             blue=config.official_blue[2], red=config.official_red[2], amber=config.official_amber[2],
                             res=False, n_points=config.n_points)
    blue_official_p3 = Loader_HDF5_3.read_files(Loader_HDF5_3.blue, Loader_DC.n_points)
    red_official_p3 = Loader_HDF5_3.read_files(Loader_HDF5_3.red, Loader_DC.n_points)
    amber_official_p3 = Loader_HDF5_3.read_files(Loader_HDF5_3.amber, Loader_DC.n_points)


if __name__ == "__main__":
    main()