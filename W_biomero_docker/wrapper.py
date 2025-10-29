import numpy as np

def biomero_entry_point(args):

    # ------------ CHANGE HERE ------------
    import image_processing as IP
    IP.initiate_resources(42, 24)
    # ------------ CHANGE HERE ------------

    # LOOP HERE, the simulated loop should do:
    # - organize itself on files discovered in the input folder,
    #   and establish tuples (e.g. upon a common number-based prefix)
    # - for each tuple:
    #   - submit the tuple to the IP.process(...tuple/list...),
    #     and collect result(s)
    #   - save the result(s)
    for i in range(3):
        # fake input image, would be taken from OMERO normally
        group_input_number_i = [ np.zeros((30+i,20+2*i)) ]

        result_group_number_i = IP.process(group_input_number_i)
        # submit 'result_group_number_i' back to OMERO

    IP.release_resources()


if __name__ == '__main__':
    biomero_entry_point([])

