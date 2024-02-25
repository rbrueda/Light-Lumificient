% purpose: defines various prolog rues for setting inside and outside effectors based on conditions

% Replaces an existing fact with a new one
replace_existing_fact(OldFact, NewFact) :-
    call(OldFact), 
    !,
    retract(OldFact),
    assertz(NewFact).

% Removes an existing fact
remove_existing_fact(OldFact) :-
    call(OldFact), 
    retract(OldFact).

% Checks if an entity is outside
%outside(Id).
outside(Id) :- 
	\+ inside(Id).


% Sets the inside effectors based on a list of effectors and a value
%setInsideEffectors(Effectors, Value).
setInsideEffectors([H|T], Y) :-
    extractInsideEffectors([H|T], [], L),
    setEffectors(L, Y).

% Sets the outside effectors based on a list of effectors and a value
%setOutsideEffectors(Effectors, Value).
setOutsideEffectors([H|T], Y) :-
    extractOutsideEffectors([H|T], [], L),
    setEffectors(L, Y).

% Sets the values of a list of effectors to a specified value
%setEffectors(Effectors, Value).
setEffectors([H|T], Y) :-
    T \== [],
    !,
    setEffectors(T, Y),
	replace_existing_fact(effectorValue(H,_), effectorValue(H, Y)),
    % write in a file the line of code to set the effector H to the value Y
    open('logActions.txt', append, Stream),
    write(Stream, 'setEffector('), write(Stream, H), write(Stream, ','), write(Stream, Y), write(Stream, ').'),nl(Stream),
    close(Stream).


% Sets the value of a single effector to a specified value
setEffectors([H|_], Y) :-
    !,
	replace_existing_fact(effectorValue(H,_), effectorValue(H, Y)),
    % write in a file the line of code to set the effector H to the value Y
    open('logActions.txt', append, Stream),
    write(Stream, 'setEffector('), write(Stream, H), write(Stream, ','), write(Stream, Y), write(Stream, ').'),nl(Stream),
    close(Stream).

% Base case for setEffectors when the effectors list is empty
setEffectors(_, _).
    
% Extracts inside effectors from a list
%extractInsideEffectors(List, NewList, variable).
extractInsideEffectors([H|T], L,X) :-
    T \== [],
    inside(H),
    !,
    extractInsideEffectors(T, [H|L], X).

extractInsideEffectors([H|T], L, X) :-
    T\== [],
    \+ inside(H),
    !,
    extractInsideEffectors(T, L, X).

extractInsideEffectors([H|_], L,X) :-
    \+ inside(H),
    !,
    X = L.

extractInsideEffectors([H|_], L, X) :-
    inside(H),
    !,
    X = [H|L].

extractInsideEffectors(_, L, X) :-
    X = L.
 

% Extracts outside effectors from a list
%extractOutsideEffectors(List, NewList, variable).
extractOutsideEffectors([H|T], L,X) :-
    T \== [],
    outside(H),
    !,
    extractOutsideEffectors(T, [H|L], X).

extractOutsideEffectors([H|T], L, X) :-
    T\== [],
    \+ outside(H),
    !,
    extractOutsideEffectors(T, L, X).

extractOutsideEffectors([H|_], L,X) :-
    \+ outside(H),
    !,
    X = L.

extractOutsideEffectors([H|_], L, X) :-
    outside(H),
    !,
    X = [H|L].

extractOutsideEffectors(_, L, X) :-
    X = L.

% Sets action for specific conditions
%set(IdAction).
set(IdAction) :-  set(IdAction, _).

% Sets action for specific conditions
%set(IdAction, IdCondition).
set(IdAction, light) :- 
    sensor(SensorId_outside, light),
    outside(SensorId_outside),
    sensorValue(SensorId_outside, X),
    preference(IdAction, light, Y, Effectors),
    X >= Y,
	setOutsideEffectors(Effectors, Y),
	setInsideEffectors(Effectors, 0).

% Sets action for temp based on specified conditions    
set(IdAction, light) :- 
    sensor(SensorId_outside, light),
    outside(SensorId_outside),
    sensorValue(SensorId_outside, X),
    preference(IdAction, light, Y, Effectors),
    X < Y,
	setOutsideEffectors(Effectors, 0), 
	setInsideEffectors(Effectors, Y).

setInsideEffectors_temp(X_temp_inside, Y_temp) :-
    (X_temp_inside < Y_temp ->  setEffectors([r], Y_temp), setEffectors([ac], 0); setEffectors([ac], Y_temp), setEffectors([r], 0) ).




% Sets action for temp based on specified conditions
set(IdAction, temp) :-
    preference(IdAction, temp, Y_temp, EffectorsTemp),
    sensor(SensorId_insideTemp, temp),
    sensorValue(SensorId_insideTemp, X_inside),
    inside(SensorId_insideTemp),
    X_inside =:= Y_temp,
    !.


set(IdAction, temp) :-
    preference(IdAction, temp, Y_temp, EffectorsTemp),
    sensor(SensorId_outsideTemp, temp),
    outside(SensorId_outsideTemp),
    sensorValue(SensorId_outsideTemp, X_outside),
    sensor(SensorId_insideTemp, temp),
    inside(SensorId_insideTemp),
    sensorValue(SensorId_insideTemp, X_inside),
    X_inside < Y_temp,
    X_outside > Y_temp,
	%check the value of the sensor wind 
    sensor(SensorId_wind, wind),
    outside(SensorId_wind),
    sensorValue(SensorId_wind, X_wind),
    preference(IdAction, wind, Y_wind, EffectorsWind),
    (X_wind =< Y_wind,
    sensor(SensorId_rain, rain),
    sensorValue(SensorId_rain, X_rain),
        (X_rain =:= 0 ->
        setOutsideEffectors(EffectorsTemp, 1),
        setInsideEffectors(EffectorsTemp, 0)
        ;
        setOutsideEffectors(EffectorsTemp, 0),
        setInsideEffectors_temp(X_inside, Y_temp)
        )
    ; 
    setOutsideEffectors(EffectorsTemp, 0),
	setInsideEffectors_temp(X_inside, Y_temp)
    ).


set(IdAction, temp) :-
    preference(IdAction, temp, Y_temp, EffectorsTemp),
    sensor(SensorId_outsideTemp, temp),
    outside(SensorId_outsideTemp),
    sensorValue(SensorId_outsideTemp, X_outside),
    sensor(SensorId_insideTemp, temp),
    inside(SensorId_insideTemp),
    sensorValue(SensorId_insideTemp, X_inside),
    X_inside < Y_temp,
    X_outside < Y_temp,
	setOutsideEffectors(EffectorsTemp, 0),
	setInsideEffectors_temp(X_inside, Y_temp).


set(IdAction, temp) :-
    preference(IdAction, temp, Y_temp, EffectorsTemp),
    sensor(SensorId_outsideTemp, temp),
    outside(SensorId_outsideTemp),
    sensorValue(SensorId_outsideTemp, X_outside),
    sensor(SensorId_insideTemp, temp),
    inside(SensorId_insideTemp),
    sensorValue(SensorId_insideTemp, X_inside),
    X_inside > Y_temp,
    X_outside > Y_temp,
	setOutsideEffectors(EffectorsTemp, 0),
	setInsideEffectors_temp(X_inside, Y_temp).



% Sets action for temp based on specified conditions    
set(IdAction, temp) :-
    preference(IdAction, temp, Y_temp, EffectorsTemp),
    sensor(SensorId_outsideTemp, temp),
    outside(SensorId_outsideTemp),
    sensorValue(SensorId_outsideTemp, X_outside),
    sensor(SensorId_insideTemp, temp),
    inside(SensorId_insideTemp),
    sensorValue(SensorId_insideTemp, X_inside),
    X_inside > Y_temp,
    X_outside < Y_temp,
    %check the value of the sensor wind 
    sensor(SensorId_wind, wind),
    sensorValue(SensorId_wind, X_wind),
    preference(IdAction, wind, Y_wind, EffectorsWind),
    (X_wind > Y_wind -> 
    setOutsideEffectors(EffectorsTemp, 0), 
    setOutsideEffectors(EffectorsWind, 0), 
    setInsideEffectors_temp(X_inside, Y_temp)
    ; 
    sensor(SensorId_rain, rain),
    sensorValue(SensorId_rain, X_rain),
        (X_rain =:= 0 ->
        setOutsideEffectors(EffectorsTemp, 1),
        setOutsideEffectors(EffectorsWind, 1),
        setInsideEffectors(EffectorsTemp, 0)
        ;
        setOutsideEffectors(EffectorsTemp, 0),
        setOutsideEffectors(EffectorsWind, 0),
        setInsideEffectors_temp(X_inside, Y_temp)
        )
    ). 

% Sets action for noise based on specified conditions
set(IdAction, noise) :-
    preference(IdAction, noise, Y_noise, EffectorsNoise),
    sensor(SensorId_noise, noise),
    sensorValue(SensorId_noise, X_noise_outside),
    X_noise_outside > Y_noise,
    sensor(SensorId_insideTemp, temp),
    inside(SensorId_insideTemp),
    sensorValue(SensorId_insideTemp, X_temp_inside),
    preference(IdAction, temp, Y_temp, EffectorsTemp),
    X_temp_inside \== Y_temp,
    setOutsideEffectors(EffectorsNoise, 0),
    setInsideEffectors_temp(X_temp_inside, Y_temp).

set(IdAction, noise) :-
    preference(IdAction, noise, Y_noise, EffectorsNoise),
    sensor(SensorId_noise, noise),
    sensorValue(SensorId_noise, X_noise_outside),
    X_noise_outside > Y_noise,
    sensor(SensorId_insideTemp, temp),
    sensorValue(SensorId_insideTemp, X_temp_inside),
    preference(IdAction, temp, Y_temp, EffectorsTemp),
    X_temp_inside == Y_temp,
    setOutsideEffectors(EffectorsNoise, 0).


% Checks if an element is a member of a list
%memberCheck(Element, List).
memberCheck(H,[H|_]).
memberCheck(H,[_|T]) :- memberCheck(H,T).