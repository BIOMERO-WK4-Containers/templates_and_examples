params.local_jobs_executor = "nextflow run -c config_node.nextflow "
params.max_pending_jobs = 3

params.input_folder = "/home/ulman/devel/NextFlow/inputs"

params.group_size = 1
// NB: Chunks the input folder files into groups, each of the size above,
//     one group is one tupple'd input -> if three files are required for
//     the processing, set group_size = 3


process create_lists_of_files {
    // this statement is here only to associate SLURM settings with this process (task)
    // (has no effect in the local config)
    clusterOptions params.get('cluster_options', '')

    // estimated time needed for this process (task) to finish
    // (has no effect in the local config)
    time 115.s
    cpus 1

    input:
    path in_files_list

    script:
    """
    echo -n "submitting ${in_files_list} on " >> /dev/pts/13
    """
}


workflow {
    //file_list = channel.fromPath( "${params.input_folder}/*.tif" )
    //files_groups = file_list.buffer( size:params.group_size, remainder:true )

    println("CONSIDERING "+params.group_size+"-TUPLES...")

    if (params.get('max_pending_jobs',-9897) == -9897) { //includes() would be better
        println("LOCAL IMMEDIATE WORKING...")

        files_groups = channel.fromPath( "${params.input_folder}/*.tif" )
            .buffer( size:params.group_size, remainder:true )
            //.view( gr -> println(gr) )

        //process_list_of_files( files_groups )
        echo_somewhere( files_groups )
    } else {
        println("SUBMITTING JOBS...")

        groups_size = params.group_size * params.get('max_forks',1)
        println("groups_size = "+groups_size)

        files_groups = channel.fromPath( "${params.input_folder}/*.tif" )
            .buffer( size:groups_size, remainder:true )
            //.view( gr -> println(gr) )

        create_lists_of_files( files_groups )
    }
}
