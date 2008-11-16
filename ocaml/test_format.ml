(* Test the Format module, which we suspect may not be working. *)

open Format

let debug = true

let () =
  let buf = Buffer.create 100 in
  let fmt = formatter_of_buffer buf in

  if debug then
    Printf.printf "pp_max_boxes before open_box = %d\n"
      (pp_get_max_boxes fmt ());

  pp_open_box fmt 0;

  if debug then
    Printf.printf "pp_max_boxes before open_box = %d\n"
      (pp_get_max_boxes fmt ());

  pp_print_string fmt "This is a string";
  pp_close_box fmt ();
  pp_print_flush fmt ();
  let str = Buffer.contents buf in
  Printf.printf "contents of buffer = %S\n%!" str
