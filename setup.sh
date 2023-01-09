mkdir -p ~/.streamlit/
echo "\
[server]\n\
headless = true\n\
port = $PORT\n\
enableCORS = true\n\
enableXsrfProtection = false\n\
\n\
" > ~/.streamlit/config.toml
