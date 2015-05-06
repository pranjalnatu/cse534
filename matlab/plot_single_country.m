A = rawOccurrences
[idx,label] = grp2idx(sort(A)) 

hist(idx,unique(idx));
set(gca,'xTickLabel',label)
ylabel('Number of Occurrences')
xlabel('Countries')
