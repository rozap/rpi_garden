var gulp = require('gulp'),
    less = require('gulp-less'),
    uglify = require('gulp-uglify'),
    spawn = require('child_process').spawn,
    minifyCSS = require('gulp-minify-css'),
    node;

var paths = {
    clientScripts: ['./static/js/**/*.js', './static/**/*.js'],
    less: ['./static/*.less'],
    css: './static/',
};


gulp.task('scripts', function() {
    console.log("UGLIFYING")
    gulp.src(paths.clientScripts)
        .pipe(uglify())
        .pipe(gulp.dest('./static/js/min/'))
});

gulp.task('less', function() {
    console.log("Rebuilding less files...");
    gulp.src(paths.css + 'style.less')
        .pipe(less({
            paths: ['style.less']
        }))
        .pipe(minifyCSS())
        .pipe(gulp.dest(paths.css));
});


gulp.task('watch', function() {
    gulp.watch(paths.clientScripts, ['scripts']);
    gulp.watch(paths.less, ['less']);
});



gulp.task('default', ['less', 'watch', 'scripts'])