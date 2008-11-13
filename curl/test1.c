/* Test using curl to fetch pages, look at headers, cookies. */

#include <stdio.h>
#include <stdlib.h>

#include <curl/curl.h>

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

int
main ()
{
  CURLcode r;
  CURL *curl;
  long code;

  r = curl_global_init (CURL_GLOBAL_ALL);
  if (r != 0) {
    fprintf (stderr, "curl_global_init failed with code %d\n", r);
    exit (1);
  }

  curl = curl_easy_init ();
  if (curl == NULL) {
    fprintf (stderr, "curl_easy_init failed\n");
    exit (1);
  }

  r = curl_easy_setopt (curl, CURLOPT_URL, url);
  if (r != CURLE_OK) {
    fprintf (stderr, "curl_easy_setopt CURLOPT_URL failed with code %d\n", r);
    exit (1);
  }

  r = curl_easy_setopt (curl, CURLOPT_WRITEFUNCTION, write_fn);
  if (r != CURLE_OK) {
    fprintf (stderr, "curl_easy_setopt CURLOPT_WRITEFUNCTION failed with code %d\n", r);
    exit (1);
  }

  r = curl_easy_setopt (curl, CURLOPT_HEADERFUNCTION, header_fn);
  if (r != CURLE_OK) {
    fprintf (stderr, "curl_easy_setopt CURLOPT_HEADERFUNCTION failed with code %d\n", r);
    exit (1);
  }

  /* This enables cookie handling in libcurl: */
  r = curl_easy_setopt (curl, CURLOPT_COOKIEFILE, "");
  if (r != CURLE_OK) {
    fprintf (stderr, "curl_easy_setopt CURLOPT_COOKIEFILE failed with code %d\n", r);
    exit (1);
  }

  /* Fetch the page. */
  printf ("fetching %s ...\n", url);
  r = curl_easy_perform (curl);
  if (r != CURLE_OK) {
    fprintf (stderr, "curl_easy_perform failed with code %d\n", r);
    exit (1);
  }
  printf ("... ok, bytes received in body was %d\n", bytes_received);

  r = curl_easy_getinfo (curl, CURLINFO_RESPONSE_CODE, &code);
  if (r != CURLE_OK) {
    fprintf (stderr, "curl_easy_getinfo CURLINFO_RESPONSE_CODE failed with code %d\n", r);
    exit (1);
  }
  printf ("HTTP response code: %d\n", (int) code);

  curl_easy_cleanup (curl);
  curl_global_cleanup ();
  exit (0);
}
