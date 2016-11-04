signature SETTINGS =
sig
    structure G : ESTGAME
    val search_depth : int
end

functor AlphaBeta (Settings : SETTINGS) : PLAYER =
struct

    exception NYI

    structure Game = Settings.G

    (* abbreviate Game as G, to keep the notation simple below. *)
    structure G = Game

    type edge  = G.move * G.est

    (* Implicit ordering:   NEGINF < Bound(v) < POSINF for all v *)
    datatype bound = NEGINF | Bound of G.est | POSINF
    type alphabeta = bound * bound    (* invariant: alpha < beta *)

    datatype orderAB = BELOW | INTERIOR | ABOVE

    (* the following ToString functions my be helpful in testing *)
    fun valueToString v = "Value(" ^ G.Est.toString v ^ ")"

    fun edgeToString (m, v) = "Edge(" ^ G.move_to_string m ^ ", " ^ G.Est.toString v ^ ")"

    fun boundToString NEGINF = "NEGINF"
      | boundToString POSINF = "POSINF"
      | boundToString (Bound v) = "Bound(" ^ G.Est.toString v ^ ")"

    fun abToString (a,b) = "(" ^ boundToString a ^ "," ^ boundToString b ^ ")"

    (* lesseq : G.est * G.est -> bool *)
    fun lesseq(x, y) = (x=y) orelse
         case (x, y) of
              (G.Est.MinnieWins, _) => true
            | (_, G.Est.MaxieWins) => true
            | (G.Est.Guess n, G.Est.Guess m) => (n <= m)
            | (_, _) => false


    (* compareAB : alphabeta -> G.est -> orderAB    *)
    (* compareAB (a,b) v  ==>                       *)
    (*                 BELOW      if  v <= a        *)
    (*                 INTERIOR   if  a < v < b     *)
    (*                 ABOVE      if  v >= b        *)
    fun compareAB (a,b) v =
      case (a, b) of
        (NEGINF, POSINF) => INTERIOR
      | (NEGINF, Bound t) => (case G.Est.compare(v, t) of
                               LESS => INTERIOR
                             |   _  => ABOVE)
      | (Bound t, POSINF) =>(case G.Est.compare(v, t) of
                               GREATER => INTERIOR
                             |   _ => BELOW)
      | (Bound l, Bound u) =>
          (case (lesseq(v, l),  (* l <= v *)
                 G.Est.compare(l, v) = LESS andalso G.Est.compare(v, u) = LESS,
                                (* l < v and v < u *)
                 lesseq(u, v))   (* u < v or v >= u *) of
            (true, _, _ ) => BELOW
         |  (_,  true, _) => INTERIOR
         |  (_,   _,true) => ABOVE
         |  (      _    ) => raise NYI)
      | (_, _) => raise NYI



    (* maxEdge : edge option -> edge -> edge option                       *)
    (* REQUIRES: true                                                     *)
    (* ENSURES:  maxEdge e1op e2 returns SOME of the edge with max value. *)
    fun maxEdge NONE e = SOME(e)
      | maxEdge (SOME(m1,v1)) (m2,v2) = SOME(if lesseq(v2,v1) then (m1,v1) else (m2,v2))

    (* minEdge : edge option -> edge -> edge option                       *)
    (* REQUIRES: true                                                     *)
    (* ENSURES:  minEdge e1op e2 returns SOME of the edge with min value. *)
    fun minEdge NONE e = SOME(e)
      | minEdge (SOME(m1,v1)) (m2,v2) = SOME(if lesseq(v1,v2) then (m1,v1) else (m2,v2))


    (* search : int -> alphabeta -> G.state -> edge option               *)
    (* REQUIRES: d > 0, (G.moves s) is nonempty.                         *)
    (* ENSURES:  search d ab s ==> SOME(optimal outgoing edge from s),   *)
    (*           based on depth-d alpha-beta prunings,                   *)
    (*           starting from alpha-beta interval "ab".                 *)
    (*                                                                   *)
    (* search uses helper functions maxisearch and minisearch to perform *)
    (* the actual search, including updating the alpha-beta interval     *)
    (* and the best edge seen so far, as well as any possible pruning.   *)
    fun search d ab s =
       case (G.player s) of
         G.Maxie => maxisearch d ab s (G.moves s) NONE
       | G.Minnie => minisearch d ab s (G.moves s) NONE



    (* maxisearch : int -> alphabeta -> G.state -> G.move Seq.seq -> edge option -> edge option *)
    (* REQUIRES: d > 0; "moves" should contain only moves that are legal at s;         *)
    (*           "s" is a Maxie state;                                                 *)
    (*           "best" should not be NONE when "moves" is Nil.                        *)
    (* ENSURES:  maxisearch d ab s moves best ==> SOME(optimal outgoing edge from s),  *)
    (*           based on depth-d alpha-beta pruning over "moves",                     *)
    (*           starting from alpha-beta interval "ab", with accumulator              *)
    (*           "best" as default if no better edge is found.                         *)
    and maxisearch d (ab as (a,b)) s moves best =
      case (Seq.showl moves) of
        Seq.Nil => best
       |Seq.Cons (m, moves') =>
          let
            (* we obtain the value returned and the edge returned *)
            val v = evaluate (d-1) ab (G.make_move (s, m))
            val edge = maxEdge best (m, v)
            (* then we compare the value with our ab to decide next step *)
           in
             case (compareAB ab v) of
               BELOW => maxisearch d ab s moves' edge (* pass *)
            |  INTERIOR => maxisearch d (Bound v, b) s moves' edge(*update*)
            |  ABOVE => edge (* prune *)
           end

    (* minisearch : int -> alphabeta -> G.state -> G.move Seq.seq -> edge option -> edge option *)
    (* REQUIRES: d > 0; "moves" should contain only moves that are legal at s;         *)
    (*           "s" is a Minnie state;                                                *)
    (*           "best" should not be NONE when "moves" is Nil.                        *)
    (* ENSURES:  minisearch d ab s moves best ==> SOME(optimal outgoing edge from s),  *)
    (*           based on depth-d alpha-beta pruning over "moves",                     *)
    (*           starting from alpha-beta interval "ab", with accumulator              *)
    (*           "best" as default if no better edge is found.                         *)
    and minisearch d (ab as (a,b)) s moves best =
      (* the overall structure is just like maxisearch *)
      case (Seq.showl moves) of
           Seq.Nil => best
        |  Seq.Cons(m, moves') =>
             let
               val v = evaluate (d-1) ab (G.make_move (s, m))
               val edge = minEdge best (m, v)
             in
               case (compareAB ab v) of
                 BELOW => edge
              | INTERIOR => minisearch d (a, Bound v) s moves' edge
              | ABOVE => minisearch d ab s moves' edge
             end


    (* evaluate : int -> alphabeta -> G.state -> G.est                     *)
    (* REQUIRES: d >= 0                                                    *)
    (* ENSURES:  evaluate d ab s ==> value attributed to state s, based on *)
    (*                               depth-d alpha-beta search.            *)
    and evaluate d ab s =
      case (G.status s, d) of
        (G.Over(G.Winner(G.Maxie)),_) => G.Est.MaxieWins
      | (G.Over(G.Winner(G.Minnie)),_) => G.Est.MinnieWins
      | (G.In_play, 0) => G.estimate s
      | (G.In_play,_) => let
                           val (SOME (move, est)) = search d ab s
                         in
                           est
                         end


    (* recall:  the signature requires that s be In_play. *)
    (* G.state -> move
     * REQUIRES: the given state is valid as the handout had specified
     * ENSURES: returns the best move going out from s *)
    fun next_move s =
      let
        val d = Settings.search_depth
        val ab = (NEGINF, POSINF)
        val SOME(move, est) = search d ab s
      in
        move
      end

end (* AlphaBeta *)
