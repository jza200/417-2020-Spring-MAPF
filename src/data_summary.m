files = ["results_8_2_CG.csv", "results_8_2_DG.csv", "results_8_2_WDG.csv", "results_8_4_CG.csv", ...
  "results_8_4_DG.csv", "results_8_4_WDG.csv", "results_16_2_CG.csv", "results_16_2_DG.csv", ...
  "results_16_2_WDG.csv", "results_16_4_CG.csv", "results_16_4_DG.csv", "results_16_4_WDG.csv", ...
  "results_16_8_CG.csv", "results_16_8_DG.csv", "results_16_8_WDG.csv", "results_64_2_CG.csv", ...
  "results_64_2_DG.csv", "results_64_2_WDG.csv"];

% Read data
d_8_2_CG = readtable(files(1));
d_8_2_DG = readtable(files(2));
d_8_2_WDG = readtable(files(3));
d_8_4_CG = readtable(files(4));
d_8_4_DG = readtable(files(5));
d_8_4_WDG = readtable(files(6));
d_16_2_CG = readtable(files(7));
d_16_2_DG = readtable(files(8));
d_16_2_WDG = readtable(files(9));
d_16_4_CG = readtable(files(10));
d_16_4_DG = readtable(files(11));
d_16_4_WDG = readtable(files(12));
d_16_8_CG = readtable(files(13));
d_16_8_DG = readtable(files(14));
d_16_8_WDG = readtable(files(15));
d_64_2_CG = readtable(files(16));
d_64_2_DG = readtable(files(17));
d_64_2_WDG = readtable(files(18));


figure(1)
% average total cpu time comparison for 2 agents 
x = [8 16];
y_CG = [mean(d_8_2_CG.Var2), mean(d_16_2_CG.Var2)];
y_DG = [mean(d_8_2_DG.Var2), mean(d_16_2_DG.Var2)];
y_WDG = [mean(d_8_2_WDG.Var2), mean(d_16_2_WDG.Var2)];
plot(x, y_CG, '-or', x, y_DG, '-sb', x, y_WDG, '-+g', 'MarkerSize', 8)
axis([6 18 0.008 0.05])
title('Average CPU time comparison for CG, DG and WDG with 2 agents')
legend('CG', 'DG', 'WDG')
xlabel('Map size')
ylabel('time(seconds)')

figure(2)
% max total cpu time comparison for 2 agents 
x = [8 16];
y_CG = [max(d_8_2_CG.Var2), max(d_16_2_CG.Var2)];
y_DG = [max(d_8_2_DG.Var2), max(d_16_2_DG.Var2)];
y_WDG = [max(d_8_2_WDG.Var2), max(d_16_2_WDG.Var2)];
plot(x, y_CG, '-or', x, y_DG, '-sb', x, y_WDG, '-+g', 'MarkerSize', 8)
axis([6 18 0 1.1])
title('Max CPU time comparison for CG, DG and WDG with 2 agents')
legend('CG', 'DG', 'WDG')
xlabel('Map size')
ylabel('time(seconds)')

figure(3)
% average total cpu time comparison for 4 agents 
x = [8 16];
y_CG = [mean(d_8_4_CG.Var2), mean(d_16_4_CG.Var2)];
y_DG = [mean(d_8_4_DG.Var2), mean(d_16_4_DG.Var2)];
y_WDG = [mean(d_8_4_WDG.Var2), mean(d_16_4_WDG.Var2)];
plot(x, y_CG, '-or', x, y_DG, '-sb', x, y_WDG, '-+g', 'MarkerSize', 8)
axis([6 18 0.05 0.38])
title('Average CPU time comparison for CG, DG and WDG with 4 agents for different map size')
legend('CG', 'DG', 'WDG')
xlabel('Map size')
ylabel('time(seconds)')

figure(4)
% max total cpu time comparison for 4 agents 
x = [8 16];
y_CG = [max(d_8_4_CG.Var2), max(d_16_4_CG.Var2)];
y_DG = [max(d_8_4_DG.Var2), max(d_16_4_DG.Var2)];
y_WDG = [max(d_8_4_WDG.Var2), max(d_16_4_WDG.Var2)];
plot(x, y_CG, '-or', x, y_DG, '-sb', x, y_WDG, '-+g', 'MarkerSize', 8)
axis([6 18 0.2 2.6])
title('Max CPU time comparison for CG, DG and WDG with 4 agents for different map size')
legend('CG', 'DG', 'WDG')
xlabel('Map size')
ylabel('time(seconds)')

figure(5)
% average total cpu time comparison
x = [2 4 8];
y_CG = [mean(d_16_2_CG.Var2), mean(d_16_4_CG.Var2), mean(d_16_8_CG.Var2)];
y_DG = [mean(d_16_2_DG.Var2), mean(d_16_4_DG.Var2), mean(d_16_8_DG.Var2)];
y_WDG = [mean(d_16_2_WDG.Var2), mean(d_16_4_WDG.Var2), mean(d_16_8_WDG.Var2)];
plot(x, y_CG, '-or', x, y_DG, '-sb', x, y_WDG, '-+g', 'MarkerSize', 8)
axis([6 18 0.05 0.38])
title('Average CPU time comparison for CG, DG and WDG with different agents for 16x16 map')
legend('CG', 'DG', 'WDG')
xlabel('Number of agents')
ylabel('time(seconds)')

figure(6)
% max total cpu time comparison
x = [2 4 8];
y_CG = [max(d_16_2_CG.Var2), max(d_16_4_CG.Var2), max(d_16_8_CG.Var2)];
y_DG = [max(d_16_2_DG.Var2), max(d_16_4_DG.Var2), max(d_16_8_DG.Var2)];
y_WDG = [max(d_16_2_WDG.Var2), max(d_16_4_WDG.Var2), max(d_16_8_WDG.Var2)];
plot(x, y_CG, '-or', x, y_DG, '-sb', x, y_WDG, '-+g', 'MarkerSize', 8)
axis([6 18 0.05 0.38])
title('Max CPU time comparison for CG, DG and WDG with different agents for 16x16 map')
legend('CG', 'DG', 'WDG')
xlabel('Number of agents')
ylabel('time(seconds)')

figure(7)
% average total cpu time comparison for 2 agents 
x = [8 16];
y_CG = [mean(d_8_4_CG.Var8), mean(d_16_4_CG.Var8)];
y_DG = [mean(d_8_4_DG.Var8), mean(d_16_4_DG.Var8)];
y_WDG = [mean(d_8_4_WDG.Var8), mean(d_16_4_WDG.Var8)];
plot(x, y_CG, '-or', x, y_DG, '-sb', x, y_WDG, '-+g', 'MarkerSize', 8)
axis([6 18 0 10])
title('Average number of expanded nodes comparison for CG, DG and WDG with 4 agents')
legend('CG', 'DG', 'WDG')
xlabel('Map size')
ylabel('number of expanded nodes')

figure(8)
% max expanded nodes comparison for both 4 agents 
x = [8 16];
y_CG = [max(d_8_4_CG.Var8), max(d_16_4_CG.Var8)];
y_DG = [max(d_8_4_DG.Var8), max(d_16_4_DG.Var8)];
y_WDG = [max(d_8_4_WDG.Var8), max(d_16_4_WDG.Var8)];
plot(x, y_CG, '-or', x, y_DG, '-sb', x, y_WDG, '-+g', 'MarkerSize', 8)
axis([6 18 0 100])
title('Max number of expanded nodes comparison for CG, DG and WDG with 4 agents')
legend('CG', 'DG', 'WDG')
xlabel('Map size')
ylabel('number of expanded nodes')

figure(9)
% average construct MDD time comparison for 4 agents 
x = [8 16];
y_CG = [mean(d_8_4_CG.Var4), mean(d_16_4_CG.Var4)];
y_DG = [mean(d_8_4_DG.Var4), mean(d_16_4_DG.Var4)];
y_WDG = [mean(d_8_4_WDG.Var4), mean(d_16_4_WDG.Var4)];
plot(x, y_CG, '-or', x, y_DG, '-sb', x, y_WDG, '-+g', 'MarkerSize', 8)
axis([6 18 0 0.5])
title('Average constructing MDD time comparison for CG, DG and WDG with 4 agents')
legend('CG', 'DG', 'WDG')
xlabel('Map size')
ylabel('time(seconds)')

figure(10)
% max expanded nodes comparison for both 4 agents 
x = [8 16];
y_CG = [max(d_8_4_CG.Var4), max(d_16_4_CG.Var4)];
y_DG = [max(d_8_4_DG.Var4), max(d_16_4_DG.Var4)];
y_WDG = [max(d_8_4_WDG.Var4), max(d_16_4_WDG.Var4)];
plot(x, y_CG, '-or', x, y_DG, '-sb', x, y_WDG, '-+g', 'MarkerSize', 8)
axis([6 18 0 2.5])
title('Max constructing MDD time comparison for CG, DG and WDG with 4 agents')
legend('CG', 'DG', 'WDG')
xlabel('Map size')
ylabel('time(seconds)')

figure(11)
% average construct MDD time comparison for 4 agents 
x = [8 16];
y_CG = [mean(d_8_4_CG.Var5), mean(d_16_4_CG.Var5)];
y_DG = [mean(d_8_4_DG.Var5), mean(d_16_4_DG.Var5)];
y_WDG = [mean(d_8_4_WDG.Var5), mean(d_16_4_WDG.Var5)];
plot(x, y_CG, '-or', x, y_DG, '-sb', x, y_WDG, '-+g', 'MarkerSize', 8)
axis([6 18 0 0.01])
title('Average update MDD time comparison for CG, DG and WDG with 4 agents')
legend('CG', 'DG', 'WDG')
xlabel('Map size')
ylabel('time(seconds)')

figure(12)
% max expanded nodes comparison for both 4 agents 
x = [8 16];
y_CG = [max(d_8_4_CG.Var5), max(d_16_4_CG.Var5)];
y_DG = [max(d_8_4_DG.Var5), max(d_16_4_DG.Var5)];
y_WDG = [max(d_8_4_WDG.Var5), max(d_16_4_WDG.Var5)];
plot(x, y_CG, '-or', x, y_DG, '-sb', x, y_WDG, '-+g', 'MarkerSize', 8)
axis([6 18 0 0.1])
title('Max update MDD time comparison for CG, DG and WDG with 4 agents')
legend('CG', 'DG', 'WDG')
xlabel('Map size')
ylabel('time(seconds)')
