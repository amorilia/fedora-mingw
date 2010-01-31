#include "example.h"

int main(void) {
  if (test() != 314) {
    return 1; /* signal error */
  } else {
    return 0;
  };
}

