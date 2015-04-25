# Build executables with all objects from libssl.a and libcrypto.a

CC=/home/hpjoshi/projects/clang

SSL_OBJ=./ssl_obj
CRYPTO_OBJ=./crypto_obj

OBF_SSL_OBJ=./obf_ssl_obj
OBF_CRYPTO_OBJ=./obf_crypto_obj

all: hello_ssl obf_hello_ssl

hello_ssl: hello_ssl.o $(SSL_OBJ)/*.o $(CRYPTO_OBJ)/*.o
	$(CC) -o hello_ssl hello_ssl.o $(SSL_OBJ)/*.o $(CRYPTO_OBJ)/*.o -ldl

obf_hello_ssl: hello_ssl.o
	$(CC) -o obf_hello_ssl hello_ssl.o $(OBF_SSL_OBJ)/*.o \
	$(OBF_CRYPTO_OBJ)/*.o -ldl

hello_ssl.o:
	$(CC) -c hello_ssl.c

clean:
	rm -f hello_ssl.o hello_ssl obf_hello_ssl
