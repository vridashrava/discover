module.exports = function(grunt) {
    grunt.initConfig({
        pkg: grunt.file.readJSON("package.json"),
        copy: {
            foundation: {
                expand: true,
                cwd: "node_modules/",
                src: ["foundation-sites/dist/**/*.js"],
                dest: "eComCrawl/static/js/"
            },
            jquery: {
                expand: true,
                cwd: "node_modules/",
                src: ["jquery/dist/*"],
                dest: "eComCrawl/static/js/"
            },
            fontawesome_font: {
                expand: true,
                cwd: "node_modules/font-awesome/fonts/",
                src: ["*"],
                dest: "eComCrawl/static/font/fontawesome"
            },
            fontawesome_scss: {
                expand: true,
                cwd: "node_modules/font-awesome/scss/",
                src: ["*"],
                // flatten: true,
                dest: "eComCrawl/static/scss/fontawesome"
            },
            chartjs: {
                expand: true,
                cwd: "node_modules/chart.js/dist/",
                src: ["Chart.min.js"],
                // flatten: true,
                dest: "eComCrawl/static/js/chart.js"
            }
            // uglify: {
            //     options: {
            //         compress: true,
            //         mangle: true,
            //         sourceMap: true
            //     },
            //     target: {
            //         src: '<%= paths.src.js %>',
            //         dest: '<%= paths.dest.jsMin %>'
            //     }
            // },
            // concat: {
            //     options: {
            //         separator: ';',
            //     },
            //     dist: {
            //         src: ['src/intro.js', 'src/project.js', 'src/outro.js'],
            //         dest: 'dist/built.js',
            //     },
            // },
        }
    })
    grunt.loadNpmTasks("grunt-contrib-copy");
    grunt.registerTask("default", []);
};
