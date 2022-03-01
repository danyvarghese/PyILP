%%%%%%%%%% tell metagol to use the BK %%%%%%%%%% 
body_pred(car/1).
body_pred(shape/1).
body_pred(train/1).
body_pred(short/1).
body_pred(closed/1).
body_pred(long/1).
body_pred(open_car/1).
body_pred(load/3).
body_pred(wheels/2).
body_pred(has_car/2).
body_pred(double/1).
body_pred(jagged/1).
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%% metarules %%%%%%%%%%%%%%%%%%%%
metarule([P,Q], [P,A],[[Q,A]]).
metarule([P,Q,R], [P,A], [[Q,A],[R,A]]).
metarule([P,Q,R], [P,A], [[Q,A,B],[R,B]]).
metarule([P,Q], [P,A,B], [[Q,A,B]]).
metarule([P,Q,R], [P,A,B], [[Q,A,B],[R,B]]).
metarule([P,Q,X], [P,A], [[Q,A,X]]).
metarule([P,Q,X], [P,A,B], [[Q,A,B,X]]).
