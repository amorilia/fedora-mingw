/* Test using curl to fetch pages, look at headers, cookies. */

#include <stdio.h>
#include <stdlib.h>

#include <curl/curl.h>

static const char *cainfo = "/etc/pki/tls/certs/ca-bundle.crt";
static const char *url = "https://fedoraproject.org/wiki/MinGW";

static int bytes_received = 0;

static size_t
write_fn (void *ptr, size_t size, size_t nmemb, void *stream)
{
  int bytes = size * nmemb;
  bytes_received += bytes;
  return bytes;
}

static size_t
header_fn (void *ptr, size_t size, size_t nmemb, void *stream)
{
  int bytes = size * nmemb;
  int i;

  /* Note that we are called once for each header, but the
   * header data is not NUL-terminated.  However we expect each
   * header is terminated by \r\n.  Hence:
   */
  for (i = 0; i < bytes; ++i)
    putchar (((char *)ptr)[i]);

  return bytes;
}

/* Handle curl errors. */
#define CHECK_ERROR(fn, args)						\
  do {									\
    CURLcode r = fn args;						\
    if (r != CURLE_OK) {						\
      fprintf (stderr, "%s: %s\n", #fn, curl_easy_strerror (r));	\
      exit (1);								\
    }									\
  } while (0)

int
main ()
{
  CURL *curl;
  long code;
  char error[CURL_ERROR_SIZE];

  CHECK_ERROR (curl_global_init, (CURL_GLOBAL_ALL));

  curl = curl_easy_init ();
  if (curl == NULL) {
    fprintf (stderr, "curl_easy_init failed\n");
    exit (1);
  }

  CHECK_ERROR (curl_easy_setopt, (curl, CURLOPT_URL, url));
  CHECK_ERROR (curl_easy_setopt, (curl, CURLOPT_CAINFO, cainfo));
  CHECK_ERROR (curl_easy_setopt, (curl, CURLOPT_WRITEFUNCTION, write_fn));
  CHECK_ERROR (curl_easy_setopt, (curl, CURLOPT_HEADERFUNCTION, header_fn));
  /* This enables error messages in curl_easy_perform: */
  CHECK_ERROR (curl_easy_setopt, (curl, CURLOPT_ERRORBUFFER, error));
  /* This enables cookie handling in libcurl: */
  CHECK_ERROR (curl_easy_setopt, (curl, CURLOPT_COOKIEFILE, ""));

  /* Fetch the page. */
  printf ("fetching %s ...\n", url);
  CHECK_ERROR (curl_easy_perform, (curl));
  printf ("... ok, bytes received in body was %d\n", bytes_received);

  CHECK_ERROR (curl_easy_getinfo, (curl, CURLINFO_RESPONSE_CODE, &code));
  printf ("HTTP response code: %d\n", (int) code);

  curl_easy_cleanup (curl);
  curl_global_cleanup ();
  exit (0);
}
