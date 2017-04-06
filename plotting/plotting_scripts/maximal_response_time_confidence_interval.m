max_mean = [
9.26739509105 6.65891779789;
26.8349722222 13.7481860552;
15.6617997543 9.84137655763;
9.44415277778 6.60714342949;
9.24185560859 6.78899796748;
9.37515205371 6.39169463087;
9.58346682848 6.71335149314;
9.4910235732 6.50417078189;
9.32177462121 6.64290665064;
9.08379069767 6.84552059497;
9.66431989924 6.75544724771;
9.13301007557 6.627673454;
];
max_error = [
3.37503919787 2.27338554832;
5.14338969458 3.91204610665;
4.54303088883 2.71697676067;
3.35301267553 2.178851984;
2.94508302143 2.18780784717;
2.97719554124 2.25590533989;
3.30141950809 2.32111249957;
3.53811930831 2.23209188225;
3.2715180175 2.25060769188;
3.15719312467 2.34725543973;
3.4836248963 2.23231216374;
3.23733612732 2.2945217765;
];

h = bar(max_mean);
set(h,'BarWidth',1);    % The bars will now touch each other
set(gca,'YGrid','on')
set(gca,'GridLineStyle','-')
%set(gca,'XTicklabel','Modelo1|Modelo2|Modelo3')
set(get(gca,'YLabel'),'String','U')
lh = legend('Our Solution','iASK');
set(lh,'Location','BestOutside','Orientation','horizontal')
hold on;
numgroups = size(max_mean, 1); 
numbars = size(max_mean, 2); 
groupwidth = min(0.8, numbars/(numbars+1.5));
legend('Our Solution', 'iASK');
xlabel('Run');
ylabel('Maximal Response Time (hr)');  
for i = 1:numbars
      % Based on barweb.m by Bolu Ajiboye from MATLAB File Exchange
      x = (1:numgroups) - groupwidth/2 + (2*i-1) * groupwidth / (2*numbars);  % Aligning error bar with individual bar
      errorbar(x, max_mean(:,i), max_error(:,i), 'k', 'linestyle', 'none');
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