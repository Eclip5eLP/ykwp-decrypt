#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>

#include "aes.h"

typedef struct {
    const char    *ext_in;
    const char    *ext_out;
    const uint8_t *key;
} crypt_params_t;

/* Constant keys for sound and encrypted zips */
const uint8_t sound_key[] = { 0x80, 0xF0, 0x08, 0x39, 0x4E, 0xB0, 0x2F, 0x4F, 0xC7, 0xF5, 0xA5, 0xC2, 0x35, 0xC4, 0x29, 0x18 };
const uint8_t zip_key[]    = { 0x2A, 0xB5, 0x11, 0xF4, 0x77, 0x97, 0x7D, 0x25, 0xCF, 0x6F, 0x7A, 0x8A, 0xE0, 0x49, 0xA1, 0x25 };
const uint8_t cud_key[]   = { 0xA3, 0x3C, 0x77, 0x8C, 0x0A, 0x62, 0x5B, 0xEC, 0x69, 0x43, 0x10, 0xC2, 0xFE, 0x21, 0x56, 0x29 };
const uint8_t ejs_key[]   = { 0x08, 0xC5, 0xC1, 0xBC, 0xC3, 0x1A, 0xE0, 0x85, 0xEF, 0x39, 0x93, 0x25, 0x07, 0x24, 0x2B, 0x6A };
const uint8_t ojk_key[]   = { 0x4F, 0xA8, 0xB9, 0x00, 0xF4, 0x92, 0x28, 0xBD, 0xA7, 0xD9, 0xC5, 0x25, 0xEF, 0x12, 0x61, 0x1D };

/* Input extension, output extension, key */
const crypt_params_t params[] = {
    { "og", "ogg", sound_key },
    { "m4", "m4a", sound_key },
    { "ez", "zip", zip_key   },
    { "cud", "json", cud_key },
    { "ayd", "zip", zip_key  },
    { "ejs", "json", ejs_key },
    { "ojk", "zip", ojk_key  }
};

/* Isolate file extension */
char *get_file_ext(char *filename) {
    char *ptr;
    size_t len;
    
    ptr = NULL;
    len = strlen(filename);
    
    while (--len)
    {
        if (filename[len] == '.')
            ptr = &filename[len + 1];
    }
    
    return ptr;
}

/* Find the true last AES block length (for unpadding PKCS#7) */
int last_block_len(uint8_t *block) {
    int i, len;
    
    len = block[15];
    
    if (len == 0 || len > 15)
        return 16; /* Not padded */
    
    for (i = 15 - 1; i > 15 - len; i--) {
        if (block[i] != len)
            return 16; /* Not padded */
    }
    
    return len;
}

int main(int argc, char **argv) {
    struct AES_ctx aes;
    const crypt_params_t *param;
    char *ext;
    char fn[FILENAME_MAX];
    FILE *in, *out;
    uint8_t iv[AES_KEYLEN];
    uint8_t *buf;
    int i, len;
    
    if (argc != 2) {
        printf("Usage: %s input\n", argv[0]);
        return 0;
    }
    
    if ((in = fopen(argv[1], "rb")) == NULL) {
        perror("Error opening input");
        return 1;
    }
    
    if ((ext = get_file_ext(argv[1])) == NULL) {
        fprintf(stderr, "File %s doesn't have an extension!\n", argv[1]);
        return 1;
    }
    
    /* Find file extension match */
    for (param = NULL, i = 0; i < 7; i++) {
        if (strcmp(ext, params[i].ext_in) == 0) {
            param = &params[i]; 
            break;
        }
    }
    
    if (param == NULL) {
        fprintf(stderr, "Unknown file extension %s!\n", ext);
        return 1;
    }
    
    /* Build output filename */
    memset(fn, 0, FILENAME_MAX);
    strncpy(fn, argv[1], ext - argv[1]);
    strcat(fn, param->ext_out);
    
    if ((out = fopen(fn, "wb")) == NULL) {
        perror("Error opening output");
        return 1;
    }
    
    /* Read in IV and initialise AES context */
    fread(iv, 1, AES_KEYLEN, in);
    AES_init_ctx_iv(&aes, param->key, iv);
    
    /* Calculate data size and allocate buffer */
    fseek(in, 0, SEEK_END);
    len = ftell(in) - AES_KEYLEN;
    buf = malloc(len);
    
    /* Seek to data start and read to buffer */
    fseek(in, AES_KEYLEN, SEEK_SET);
    fread(buf, 1, len, in);
    fclose(in);
    
    /* Decrypt data */
    AES_CBC_decrypt_buffer(&aes, buf, len);
    
    /* Remove padding from last block */
    len -= last_block_len(buf + len - AES_BLOCKLEN);
    
    /* Write decrypted data */
    fwrite(buf, 1, len, out);
    fclose(out);
    
    free(buf);
    
    printf("Successfully decrypted %s to %s!\n", argv[1], fn);
    
    return 0;
}
