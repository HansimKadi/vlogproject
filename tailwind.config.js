/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './vlogpost/templates/vlogpost/vlogpost_form.html',
    './vlogpost/templates/vlogpost/vlog_detail.html',
    './vlogpost/templates/vlogpost/vlogpost_list.html',
    './vlogpost/templates/base.html',
    './static/scripts/main.js', //             // Includes all JavaScript files in static
  ],
  theme: {
    extend: {},
  },
  plugins: [],
};
