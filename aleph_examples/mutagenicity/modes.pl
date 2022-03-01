:- aleph_set(noise, 5).
:- aleph_set(i,2).
:- aleph_set(minpos,2).
:- aleph_set(clauselength,4).






:- modeh(*, active(+drug)).

:- modeb(*,atm(+drug,-atomid,#element,#int,-charge)).
:- modeb(*,bond(+drug,-atomid,-atomid,#int)).
:- modeb(*,bond(+drug,+atomid,-atomid,#int)).
:- modeb(*,gteq(+charge,#float)).
:- modeb(*,gteq(+energy,#float)).
:- modeb(*,gteq(+hydrophob,#float)).
:- modeb(*,gteq(+float,#float)).
:- modeb(*,lteq(+charge,#float)).
:- modeb(*,lteq(+energy,#float)).
:- modeb(*,lteq(+hydrophob,#float)).
:- modeb(*,lteq(+float,#float)).
:- modeb(*,value_of(+charge,#charge)).
:- modeb(*,value_of(+energy,#energy)).
:- modeb(*,value_of(+hydrophob,#hydrophob)).
:- modeb(*,ind1(+drug,#int)).
:- modeb(*,inda(+drug,#int)).
:- modeb(*,lumo(+drug,-energy)).
:- modeb(*,logp(+drug,-hydrophob)).

:- modeb(1,benzene(+drug,-ring)).
:- modeb(1,carbon_5_aromatic_ring(+drug,-ring)).
:- modeb(1,carbon_6_ring(+drug,-ring)).
:- modeb(1,hetero_aromatic_6_ring(+drug,-ring)).
:- modeb(*,hetero_aromatic_5_ring(+drug,-ring)).
:- modeb(*,ring_size_6(+drug,-ring)).
:- modeb(*,ring_size_5(+drug,-ring)).
:- modeb(*,nitro(+drug,-ring)).
:- modeb(*,methyl(+drug,-ring)).
:- modeb(*,anthracene(+drug,-ringlist)).
:- modeb(*,phenanthrene(+drug,-ringlist)).
:- modeb(*,ball3(+drug,-ringlist)).





:- determination(active/1,atm/5).
:- determination(active/1,bond/4).
:- determination(active/1,gteq/2).
:- determination(active/1,lteq/2).
:- determination(active/1,value_of/2).

:- determination(active/1,ind1/2).
:- determination(active/1,inda/2).

:- determination(active/1,lumo/2).
:- determination(active/1,logp/2).

:- determination(active/1,benzene/2).
:- determination(active/1,carbon_5_aromatic_ring/2).
:- determination(active/1,carbon_6_ring/2).
:- determination(active/1,hetero_aromatic_6_ring/2).
:- determination(active/1,hetero_aromatic_5_ring/2).
:- determination(active/1,ring_size_6/2).
:- determination(active/1,ring_size_5/2).
:- determination(active/1,nitro/2).
:- determination(active/1,methyl/2).
:- determination(active/1,anthracene/2).
:- determination(active/1,phenanthrene/2).
:- determination(active/1,ball3/2).
:- determination(active/1,member/2).
:- determination(active/1,connected/2).

