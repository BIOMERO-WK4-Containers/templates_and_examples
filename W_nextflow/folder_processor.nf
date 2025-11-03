params.processor = "/home/ulman/data/Kobe-Hackathon/seg_and_tra_pipeline/W_nextflow/processor.sh"
params.input_folder = "/home/ulman/devel/NextFlow/inputs"
params.output_folder = "/home/ulman/devel/NextFlow/outputs"

params.group_size = 1
// NB: Chunks the input folder files into groups, each of the size above,
//     one group is one tupple'd input -> if three files are required for
//     the processing, set group_size = 3

// how many parallel instances are permitted at one moment:
// - in local config: not more than that processes are created
params.max_forks = 5


process process_list_of_files {
    maxForks params.max_forks
    publishDir params.output_folder

    input:
    path in_files_list

    output:
    path 'res_of_*'

    script:
    """
    echo -n "processing ${in_files_list} on " >> /dev/pts/13
    date >> /dev/pts/13
    hostname >> /dev/pts/13
    sleep 2
    ${params.processor} ${in_files_list}
    echo -n "finished   ${in_files_list} on " >> /dev/pts/13
    date >> /dev/pts/13
    """
}


process echo_somewhere {
    input:
    path in_files_list

    script:
    """
    echo "$in_files_list" >> /dev/pts/13
    """
}


workflow {
    file_list = channel.fromPath( "${params.input_folder}/*.tif" )
    files_groups = file_list.buffer( size:params.group_size, remainder:true )

    //process_list_of_files( files_groups )
    echo_somewhere( files_groups )
}
