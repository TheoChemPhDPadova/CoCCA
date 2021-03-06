"""Trajectory Pruner"""
import sys, os
import utils


def main():
    def multiple_parser(inp_list):
        """Multiple input parser"""
        out_list = []
        for k in inp_list:
            if "-" in k:
                for li in range(int(k.split("-")[0]), int(k.split("-")[1]) + 1):
                    if int(li) not in out_list:
                        out_list.append(int(li))
            else:
                if int(k) not in out_list:
                    out_list.append(int(k))
        return out_list

    utils.TITLE("Trajectory Pruning")

    TRJ = utils.TRJ(input("Enter trajectory file path...\t"))
    K_LIST = input("\nSnapshot groups to extract? (e.g. 1-5 6-10)\t").split()
    K_LISTD = [multiple_parser([i]) for i in K_LIST]

    for trj_n, sna_list in enumerate(K_LISTD):
        with open("./TRJ_{}.xyz".format(str(trj_n)), 'a') as out:
            for idx_i, val_i in enumerate(TRJ.trajectory):
                if idx_i + 1 in sna_list:
                    out.write("{}\n".format(str(TRJ.natoms)))
                    out.write("Trajectory {}\n".format(idx_i + 1))
                    for j in val_i:
                        out.write("{} \t{:.10f}\t {:.10f}\t {:.10f} \n".format(j[0], j[1], j[2], j[3]))
    utils.NT()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Interrupted by user")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
