(* From: http://www.ocaml-tutorial.org/the_structure_of_ocaml_programs *)

open Graphics;;

let () =
  open_graph " 640x480";
  for i = 12 downto 1 do
    let radius = i * 20 in
    set_color (if (i mod 2) = 0 then red else yellow);
    fill_circle 320 240 radius
  done;
  ignore (read_line ())
