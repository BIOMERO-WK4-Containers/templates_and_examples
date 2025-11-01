params.processor = "/home/ulman/devel/NextFlow/test2/processor.sh"
params.input_folder = "/home/ulman/devel/NextFlow/inputs"
params.output_folder = "/home/ulman/devel/NextFlow/outputs"

params.group_size = 1
// NB: Chunks the input folder files into groups, each of the size above,
//     one group is one tupple'd input -> if three files are required for
//     the processing, set group_size = 3

// how many parallel instances are permitted at one moment:
// - in local config: not more than that processes are created
// - in SLURM config: not more than that jobs are executed and waiting
params.max_forks = 5
params.cluster_options = ''


process process_list_of_files {
    maxForks params.max_forks

    // this statement is here only to associate SLURM settings with this process (task)
    // (has no effect in the local config)
    clusterOptions params.cluster_options

    // estimated time needed for this process (task) to finish
    // (has no effect in the local config)
    time 115.s
    cpus 1

    publishDir params.output_folder

    input:
    path in_files_list

    output:
    path 'res_of_*'

    script:
    """
    echo -n "processing ${in_files_list} on "
    date
    hostname
    sleep 2
    ${params.processor} ${in_files_list}
    echo -n "finished   ${in_files_list} on "
    date
    """
}


workflow {
    file_list = channel.fromPath( "${params.input_folder}/*.tif" )
    files_groups = file_list.buffer( size:params.group_size, remainder:true )

    process_list_of_files( files_groups )
}
