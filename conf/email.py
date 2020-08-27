


#EMAIL_BACKEND = "sendgrid_backend.SendgridBackend"
#SENDGRID_API_KEY = os.environ.get("SENDGRID_API_KEY")

# Remove the configuration below once we have the send grid account
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = 'henz.jmedina@gmail.com'
EMAIL_HOST_PASSWORD = 'acnwcknaescnkvwp'
