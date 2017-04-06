rate_mean = [
97.2286374134 97.5717439294;
96.9976905312 96.9631236443;
95.0934579439 97.052154195;
96.0 97.4238875878;
96.766743649 96.4705882353;
95.4751131222 96.7532467532;
98.0952380952 97.1764705882;
96.6426858513 96.6587112172;
96.2800875274 98.3451536643;
97.2850678733 97.3273942094;
96.359223301 97.7578475336;
98.024691358 96.9298245614;
];
rate_error = [
9.28772232707 8.70912900372;
9.6554801051 9.70917440498;
12.2216131048 9.57018690341;
11.087434329 8.9635610589;
10.0080296031 10.4403263946;
11.7601917317 10.0281971606;
7.7340995789 9.3722133667;
10.19168364 10.1681736596;
10.7077949788 7.2180646283;
9.19534503451 9.12536929228;
10.5976388455 8.37671682295;
7.87318890869 9.76058298459;
];
h = bar(rate_mean);
set(h,'BarWidth',1);    % The bars will now touch each other
set(gca,'YGrid','on')
set(gca,'GridLineStyle','-')
%set(gca,'XTicklabel','Modelo1|Modelo2|Modelo3')
set(get(gca,'YLabel'),'String','U')
lh = legend('Our Solution','iASK');
set(lh,'Location','BestOutside','Orientation','horizontal')
hold on;
numgroups = size(rate_mean, 1); 
numbars = size(rate_mean, 2); 
groupwidth = min(0.8, numbars/(numbars+1.5));
legend('Our Solution', 'iASK');
xlabel('Run');
ylabel('Response rate (%)');  
for i = 1:numbars
      % Based on barweb.m by Bolu Ajiboye from MATLAB File Exchange
      x = (1:numgroups) - groupwidth/2 + (2*i-1) * groupwidth / (2*numbars);  % Aligning error bar with individual bar
      errorbar(x, rate_mean(:,i), rate_error(:,i), 'k', 'linestyle', 'none');
end

set(gca,'FontSize',20)
set(gca, 'FontName', 'Times New Roman');
set(gca,'TickDir','out')
set(get(gca, 'xlabel'), 'interpreter', 'latex');
set(get(gca, 'xlabel'), 'FontName', 'Times New Roman');
set(get(gca, 'xlabel'), 'FontSize', 20);
set(get(gca, 'ylabel'), 'interpreter', 'latex');
set(get(gca, 'ylabel'), 'FontName', 'Times New Roman');
set(get(gca, 'ylabel'), 'FontSize', 20);
set(legend(), 'interpreter', 'latex');
set(legend(), 'FontName', 'Times New Roman');
set(legend(), 'FontSize', 20);
set(gcf, 'WindowStyle', 'normal');
set(gca, 'Unit', 'inches');
set(gca, 'Position', [.65 .65 4.6 3.125]);
set(gcf, 'Unit', 'inches');
set(gcf, 'Position', [0.25 2.5 5.5 4.05]);
 % for 3-column figures
set(gca,'FontSize',20)
set(gca, 'FontName', 'Times New Roman');
set(gca,'TickDir','out')
set(get(gca, 'xlabel'), 'interpreter', 'latex');
set(get(gca, 'xlabel'), 'FontName', 'Times New Roman');
set(get(gca, 'xlabel'), 'FontSize', 20);
set(get(gca, 'ylabel'), 'interpreter', 'latex');
set(get(gca, 'ylabel'), 'FontName', 'Times New Roman');
set(get(gca, 'ylabel'), 'FontSize', 20);
set(legend(), 'interpreter', 'latex');
set(legend(), 'FontName', 'Times New Roman');
set(legend(), 'FontSize', 20);
set(gcf, 'WindowStyle', 'normal');
set(gca, 'Unit', 'inches');
set(gca, 'Position', [.65 .65 4.6 3.125]);
set(gcf, 'Unit', 'inches');
set(gcf, 'Position', [0.25 2.5 5.5 4.05]);