params.processor = "/home/ulman/devel/NextFlow/test2/processor.sh"
params.input_folder = "/home/ulman/devel/NextFlow/inputs"
params.output_folder = "/home/ulman/devel/NextFlow/outputs"

params.group_size = 1
// NB: Chunks the input folder into groups, each of the size above
// (Use "mega large number" to create just one group...)


process process_list_of_files {
    publishDir params.output_folder

    input:
    path in_files_list

    output:
    path 'res_of_*'

    script:
    """
    ${params.processor} ${in_files_list}
    """
}


workflow {
    file_list = channel.fromPath( "${params.input_folder}/*.tif" )
    files_groups = file_list.buffer( size:params.group_size, remainder:true )

    process_list_of_files( files_groups )
}
