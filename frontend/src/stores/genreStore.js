import { defineStore } from "pinia";

export const useGenreStore = defineStore('genre',{
    state: () => ({
        genreMap: {
            12 : ["Adventure", "#FFD700"],              // VIBRANT YELLOW
            14 : ["Fantasy", "#8A2BE2"],                // BLUE VIOLET
            16 : ["Animation", "#FAA916"],              // ORANGE
            18 : ["Drama", "#1B1F1A"],                  // BLACK
            27 : ["Horror", "#8B0000"],                 // DARK RED
            28 : ["Action", "#FF0000"],                 // RED
            35 : ["Comedy", "#FF8C00"],                 // ORANGE
            36 : ["History", "#808000"],                // OLIVE GREEN
            37 : ["Western", "#D2691E"],                // CHOCOLATE BROWN
            53 : ["Thriller", "#000080"],               // NAVY BLUE
            80 : ["Crime", "#A9A9A9"],                  // DARK GREY
            99 : ["Documentary", "#3289D1"],            // POWDER BLUE
            878 : ["Science Fiction", "#228B22"],       // CHARTRUESE 
            9648 : ["Mystery", "#800080"],              // PURPLE
            10402 : ["Music", "#FF1493"],               // DEEP PINK
            10749 : ["Romance", "#FF69B4"],             // HOT PINK
            10751 : ["Family", "#DAA520"],              // GOLDENROD
            10752 : ["War", "#B22222"],                 // FIREBRICK
            10759 : ["Action & Adventure", "#D2B48C"],  // BROWN
            10762 : ["Kids", "#00BFFF"],                // KHAKI
            10763 : ["News", "#4682B4"],                // STEEL BLUE
            10764 : ["Reality", "#FF4500"],             // ORANGE RED
            10765 : ["Sci-Fi & Fantasy", "#3A2C8D"],    // AQUA
            10766 : ["Soap", "#E6A8D7"],                // THISTLE
            10767 : ["Talk", "#808080"],                // GREY
            10768 : ["War & Politics", "#556B2F"],      // DARK OLIVE GREEN
            10770 : ["TV Movie", "#C71585"],            // MEDIUM VIOLET RED
        },
    }),
    getters: {
        getGenreById: (state) => (id) => {
            const genre = state.genreMap[id];
            return genre ? genre[0] : 'Unknown';
        },
        getGenreColorById: (state) => (id) => {
            const genre = state.genreMap[id];
            return genre ? genre[1] : '#FFFFFF';
        },
    },
});